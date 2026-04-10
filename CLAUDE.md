# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pocket Heist is a gamified task-assignment application with a spy/heist theme. The project follows an **API-first architecture** where the FastAPI backend exposes RESTful endpoints consumed by frontend clients.

**Frontends:**
- **Phase 1 (Streamlit)**: Rapid prototyping MVP - `frontend/`
- **Phase 2 (React)**: Production-ready UI - `frontend-react/` ✅ **COMPLETED**

The API-first design enabled zero backend changes when migrating from Streamlit to React, validating the architecture.

## Architecture Principles

### API-First Design
- **Complete separation**: Backend and frontend communicate exclusively via REST API
- **Stateless authentication**: JWT tokens (24-hour expiry, HS256 algorithm)
- **CORS-enabled**: Configured for localhost:3000, localhost:5173 (Vite), and localhost:8501 (Streamlit)
- **JSON responses**: All endpoints return `application/json`
- **No shared state**: Backend has zero knowledge of frontend implementation

### Data Flow

**Streamlit (Phase 1):**
```
User → Streamlit UI → api_client.py → FastAPI Backend → SQLAlchemy → SQLite
                         (HTTP)           (Pydantic)      (ORM)
```

**React (Phase 2):**
```
User → React UI → Axios (services/) → FastAPI Backend → SQLAlchemy → SQLite
         (JSX)      (HTTP + interceptors)  (Pydantic)      (ORM)
```

## Commands

### Running the Application

**Backend (Terminal 1):**
```bash
uvicorn backend.main:app --reload
# API docs at http://127.0.0.1:8000/docs
```

**Frontend Options (Terminal 2):**

**React (Phase 2 - Recommended):**
```bash
cd frontend-react
npm install  # First time only
npm run dev
# App at http://localhost:5173
```

**Streamlit (Phase 1 - Legacy):**
```bash
streamlit run frontend/app.py
# App at http://localhost:8501
```

### Testing

**Backend Tests (pytest):**
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

**React Frontend Tests:**
```bash
cd frontend-react

# Automated API smoke test (verifies backend is ready)
bash test-api.sh

# Manual E2E testing - see:
# - E2E_TEST_CHECKLIST.md (30 test cases)
# - TESTING_GUIDE.md (setup guide)
# - TEST_RESULTS.md (results template)
```

### Development
```bash
# Backend dependencies
pip install -r backend/requirements.txt

# Streamlit frontend (Phase 1)
pip install -r frontend/requirements.txt

# React frontend (Phase 2)
cd frontend-react && npm install && cd ..

# Production build (React)
cd frontend-react && npm run build && cd ..

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

### Frontend Stack (Phase 1 - Streamlit)
- Streamlit: Rapid UI development
- requests: HTTP client for API calls
- pandas: Data display in archive view

### Frontend Stack (Phase 2 - React) ✅
- React 18: Component-based UI library with hooks
- Vite: Fast dev server and build tool
- React Router v6: Client-side routing with nested routes
- Axios: HTTP client with request/response interceptors
- Tailwind CSS v3.4: Utility-first CSS framework
- date-fns: Date formatting and manipulation
- Lucide React: Icon library
- **CRITICAL**: Tailwind CSS pinned to v3.4 (v4 causes PostCSS errors)

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

## Phase 2: React Frontend (COMPLETED) ✅

### Architecture Overview

The React frontend validates the API-first architecture by consuming the exact same backend with **zero API changes**.

**Key Decisions:**
- **No Backend Changes**: Validated API-first design - React uses same endpoints as Streamlit
- **localStorage for Auth**: JWT tokens stored in `localStorage` (replaces Streamlit's `st.session_state`)
- **Axios Interceptors**: Automatic token injection + 401 error handling with auto-redirect
- **Context API**: Global state management (AuthContext, ToastContext)
- **React Router v6**: Client-side routing with protected routes and nested layouts
- **Tailwind CSS**: Dark theme (`#0a0a0c` bg, `#f59e0b` gold accents), mobile-first responsive

### React Project Structure
```
frontend-react/src/
├── components/         # Reusable UI components
│   ├── HeistCard.jsx           # Card with status, difficulty, abort button
│   ├── HeistCardSkeleton.jsx   # Pulsing loading skeleton
│   ├── HeistDetailsModal.jsx   # Full-screen modal with backdrop
│   ├── HeistGrid.jsx           # Responsive grid (1/2/3 cols)
│   ├── ProtectedRoute.jsx      # Auth guard wrapper
│   └── Toast.jsx               # Individual toast notification
│
├── contexts/           # React Context providers
│   ├── AuthContext.jsx         # Auth state + login/register/logout
│   └── ToastContext.jsx        # Global toast notifications
│
├── layouts/            # Page layouts
│   └── DashboardLayout.jsx     # Sidebar + header + Outlet
│
├── pages/              # Route pages
│   ├── LandingPage.jsx         # Login/register (public)
│   ├── WarRoom.jsx             # Active heists
│   ├── MyAssignments.jsx       # User's heists (all statuses)
│   ├── BlueprintStudio.jsx     # Create heist form
│   └── IntelArchive.jsx        # Expired/aborted heists
│
├── services/           # API client layer
│   ├── api.js                  # Axios instance + interceptors
│   ├── auth.js                 # Register, login, logout
│   └── heists.js               # CRUD operations
│
├── App.jsx             # Root with BrowserRouter + routes
└── main.jsx            # React entry point
```

### Critical Patterns (React)

#### 1. Axios Interceptors (Request & Response)
```javascript
// Request interceptor - auto-inject JWT
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('jwt_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Response interceptor - handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.clear();
      window.location.href = '/login';  // Auto-redirect
    }
    return Promise.reject(error);
  }
);
```

#### 2. Protected Routes Pattern
```javascript
// In App.jsx
<Route path="/" element={
  <ProtectedRoute>
    <DashboardLayout />
  </ProtectedRoute>
}>
  <Route path="war-room" element={<WarRoom />} />
  <Route path="my-assignments" element={<MyAssignments />} />
  // ...
</Route>
```

#### 3. Service Layer Pattern
All API calls return consistent format:
```javascript
// services/heists.js
export const createHeist = async (data) => {
  try {
    const response = await api.post('/heists', data);
    return { success: true, data: response.data };
  } catch (error) {
    return { 
      success: false, 
      error: error.response?.data?.detail || 'Failed to create heist' 
    };
  }
};
```

Pages handle responses uniformly:
```javascript
const result = await createHeist(heistData);
if (result.success) {
  toast.success('Mission launched!');
} else {
  toast.error(result.error);
}
```

#### 4. Toast Notifications (Global Context)
```javascript
// Provide globally
<ToastProvider>
  <App />
</ToastProvider>

// Use anywhere
const toast = useToast();
toast.success('Heist aborted successfully');
toast.error('Failed to abort heist');
toast.info('Aborting mission...');
```

#### 5. Loading States with Skeletons
```javascript
// Replace spinners with skeleton grids
if (loading) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {[1, 2, 3].map((i) => <HeistCardSkeleton key={i} />)}
    </div>
  );
}
```

### Environment Variables (React)
```bash
# .env in frontend-react/
VITE_API_BASE_URL=http://127.0.0.1:8000
```

**IMPORTANT**: All Vite env vars must be prefixed with `VITE_` to be exposed to client.

### Routing Structure
```
/login              → LandingPage (public)
/                   → Redirect to /war-room
/war-room           → WarRoom (protected)
/my-assignments     → MyAssignments (protected)
/create             → BlueprintStudio (protected)
/archive            → IntelArchive (protected)
/*                  → Redirect to /
```

### Testing (React)
```bash
cd frontend-react

# Automated API smoke tests
bash test-api.sh

# Manual E2E testing
# See: E2E_TEST_CHECKLIST.md
# See: TESTING_GUIDE.md
```

Manual E2E test checklist covers:
- Authentication flow (register, login, logout)
- Heist CRUD (create, view, search, abort)
- UI polish (toasts, skeletons, animations)
- Responsive design (mobile, tablet, desktop)
- Cross-browser compatibility

### Production Build
```bash
cd frontend-react
npm run build
# Output: dist/ folder (~350 KB total)
# - CSS: 18 KB (gzip: 4.4 KB)
# - JS: 332 KB (gzip: 104 KB)

# Test production build
npm run preview
# Opens at http://localhost:4173
```

### Common React Mistakes to Avoid

1. **Don't bypass service layer**: Always use `services/heists.js`, never call `api.post()` directly from components
2. **Don't skip toast context**: Use `useToast()` instead of `alert()` or inline error states
3. **Don't hardcode API URL**: Use `import.meta.env.VITE_API_BASE_URL` from .env
4. **Don't upgrade Tailwind to v4**: Pinned to v3.4.0 for PostCSS compatibility
5. **Don't forget loading states**: Use `<HeistCardSkeleton />` grids, not spinners

## Known Technical Debt / Deprecations

- **datetime.utcnow()**: Used throughout codebase, deprecated in Python 3.12+. Future: migrate to `datetime.now(timezone.utc)`
- **SQLAlchemy declarative_base()**: Deprecated in SQLAlchemy 2.0, use `orm.declarative_base()` instead
- **Pydantic Config class**: Use `ConfigDict` instead of `class Config` for Pydantic v2+ compatibility

These deprecations generate warnings but don't affect functionality. Address them in a future refactoring sprint.
