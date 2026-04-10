# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pocket Heist is a gamified task-assignment application with a spy/heist theme. The project follows an **API-first architecture** where the FastAPI backend exposes RESTful endpoints consumed by the Streamlit frontend. This design allows future migration to React without backend changes.

## Architecture Principles

### API-First Design
- **Complete separation**: Backend and frontend communicate exclusively via REST API
- **Stateless authentication**: JWT tokens (24-hour expiry, HS256 algorithm)
- **CORS-enabled**: Configured for localhost:3000 and localhost:8501
- **JSON responses**: All endpoints return `application/json`
- **No shared state**: Backend has zero knowledge of frontend implementation

### Data Flow
```
User → Streamlit UI → api_client.py → FastAPI Backend → SQLAlchemy → SQLite
                         (HTTP)           (Pydantic)      (ORM)
```

## Commands

### Running the Application
```bash
# Backend (Terminal 1)
uvicorn backend.main:app --reload
# API docs at http://127.0.0.1:8000/docs

# Frontend (Terminal 2)
streamlit run frontend/app.py
# App at http://localhost:8501
```

### Testing
```bash
# Run test suites SEPARATELY (important - see Testing Notes below)
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/smoke/ -v

# Run specific test file
pytest tests/unit/test_auth.py -v

# Run with hypothesis statistics
pytest tests/unit/ -v --hypothesis-show-statistics
```

### Development
```bash
# Install dependencies
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# Clean test databases
rm -f test_*.db
```

## Key Architecture Decisions

### 1. Route Ordering (CRITICAL)
In `backend/routers/heists.py`, routes are ordered to prevent path conflicts:
```python
# ✅ Correct order
GET /heists
POST /heists
GET /heists/archive    # MUST come before /{id}
GET /heists/mine
GET /heists/{id}       # Generic pattern last
PATCH /heists/{id}/abort
```

If `/heists/{id}` comes before `/heists/archive`, FastAPI will treat "archive" as an ID parameter.

### 2. Deadline-Aware Filtering
Active heists are filtered at **query time**, not via background jobs:
```python
# In heist_service.py
now = datetime.utcnow()
heists = db.query(Heist).filter(
    Heist.status == HeistStatus.active,
    Heist.deadline > now  # Real-time deadline check
).all()
```

This eliminates the need for cron jobs or schedulers in Phase 1.

### 3. Authentication Flow
```python
# 1. User registers → password hashed with bcrypt
# 2. User logs in → JWT token created with exp + iat claims
# 3. Frontend stores token in st.session_state.access_token
# 4. Every API call includes: Authorization: Bearer <token>
# 5. Backend dependency get_current_user() validates and decodes JWT
```

All protected routes use `Depends(get_current_user)` to enforce authentication.

### 4. Database Models
**Two main models:**
- `User`: id, username (unique), hashed_password, created_at
- `Heist`: id, title, target, difficulty, assignee_username, creator_id (FK), deadline, description, status, created_at

**Relationships:**
- `User.heists` → one-to-many → creator's heists
- `Heist.creator` → many-to-one → User

**Important**: `assignee_username` is a string field, not a foreign key. This allows assigning heists to users who haven't registered yet (design choice for flexibility).

### 5. Enums
```python
class Difficulty(str, Enum):
    training = "Training"
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"
    legendary = "Legendary"

class HeistStatus(str, Enum):
    active = "Active"
    expired = "Expired"
    aborted = "Aborted"
```

Status transitions:
- Created → `Active`
- Creator aborts → `Aborted`
- Deadline passes → remains `Active` (filtered out of active list, appears in archive)

## Testing Notes

### Test Suite Structure
- **Unit tests** (`tests/unit/`): Business logic, validation, services
- **Integration tests** (`tests/integration/`): API endpoints end-to-end
- **Smoke tests** (`tests/smoke/`): API-first architecture validation (CORS, JSON, /docs)

### IMPORTANT: Run Test Suites Separately
Integration tests have database fixture conflicts when run all together. This is a known test infrastructure issue (multiple test files override the same FastAPI dependency). Solution:
```bash
# ✅ Run separately
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/smoke/ -v

# ❌ Avoid running all together
pytest tests/ -v  # Will have conflicts
```

### Property-Based Testing with Hypothesis
Many tests use Hypothesis for randomized inputs:
```python
@given(
    title=st.text(min_size=1, max_size=100),
    difficulty=st.sampled_from(list(Difficulty))
)
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_heist_creation(client, auth_token, title, difficulty):
    ...
```

The `suppress_health_check` is required because Hypothesis doesn't like function-scoped pytest fixtures. This is acceptable for our test design.

### Test Database Strategy
Each integration test file uses its own SQLite database:
- `test_auth_api.py` → creates unique timestamped DBs
- `test_auth_api_simple.py` → `test_simple.db`
- `test_heist_api.py` → `test_heist_api.db`
- `test_protected_routes.py` → `test_protected.db`

Databases are created/dropped per test via `@pytest.fixture(autouse=True, scope="function")`.

## Dependencies and Version Constraints

### Critical Version Pins
- **bcrypt==4.0.1**: Pinned due to compatibility issues with newer versions causing test failures
- Do not upgrade bcrypt without testing the full suite

### Backend Stack
- FastAPI: Modern async web framework
- SQLAlchemy: ORM with declarative models
- Pydantic: Request/response validation
- python-jose: JWT token creation/verification
- passlib + bcrypt: Password hashing
- hypothesis: Property-based testing
- pytest + httpx: Testing

### Frontend Stack
- Streamlit: Rapid UI development
- requests: HTTP client for API calls
- pandas: Data display in archive view

## Frontend Architecture

### API Client Pattern
`frontend/api_client.py` wraps all backend calls:
```python
def get_headers() -> Dict[str, str]:
    # Automatically includes JWT from st.session_state
    
def list_active_heists() -> List[Dict]:
    # Returns parsed JSON or empty list on error
```

**Never make direct `requests` calls from `app.py`** - always use `api_client.py` functions. This centralizes auth header logic and error handling.

### Session State Management
```python
# After login
st.session_state.access_token = "..."
st.session_state.username = "..."

# Check auth
if "access_token" not in st.session_state:
    show_login_page()
    return
```

### UI Pages
- `show_login_page()`: Login/register tabs
- `show_war_room()`: 2-column grid of active heists, abort buttons for creators
- `show_plan_new_heist()`: Heist creation form with auto-deadline (+3 hours)
- `show_my_heists()`: User's created heists
- `show_mission_archive()`: DataFrame table of expired/aborted heists

## Common Patterns

### Creating a New Heist
```python
# Backend validates
1. deadline > utcnow() (Pydantic validator)
2. difficulty in Difficulty enum
3. User is authenticated

# Backend sets
- creator_id = current_user.id
- status = HeistStatus.active
- created_at = utcnow()
```

### Aborting a Heist
```python
# Business rules enforced in heist_service.py
1. Check current_user.id == heist.creator_id (403 if not)
2. Check heist.status == Active (409 if not)
3. Transition status to Aborted
```

### Error Response Format
All API errors return:
```json
{
  "detail": "Error message here"
}
```

Status codes:
- 401: Unauthorized (missing/invalid token)
- 403: Forbidden (not the creator)
- 404: Not Found
- 409: Conflict (duplicate username, heist already aborted)
- 422: Validation Error (Pydantic)

## Future Migration Path (Phase 2: React)

When migrating to React:
1. **No backend changes required** - API contract remains identical
2. Replace Streamlit with React components
3. Replace `api_client.py` with Axios/Fetch in React
4. Use React Router for navigation (currently Streamlit radio button)
5. JWT storage: move from `st.session_state` to `localStorage` or Redux

The API-first architecture guarantees this migration is purely frontend work.

## Known Technical Debt / Deprecations

- **datetime.utcnow()**: Used throughout codebase, deprecated in Python 3.12+. Future: migrate to `datetime.now(timezone.utc)`
- **SQLAlchemy declarative_base()**: Deprecated in SQLAlchemy 2.0, use `orm.declarative_base()` instead
- **Pydantic Config class**: Use `ConfigDict` instead of `class Config` for Pydantic v2+ compatibility

These deprecations generate warnings but don't affect functionality. Address them in a future refactoring sprint.
