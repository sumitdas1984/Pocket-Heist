# Pocket Heist 🎯

> A fun, gamified task assignment application where users create and manage "heists" - tiny missions with big office mischief potential.

[![Phase 1](https://img.shields.io/badge/Phase%201-Streamlit-brightgreen)](./frontend)
[![Phase 2](https://img.shields.io/badge/Phase%202-React-blue)](./frontend-react)
[![API](https://img.shields.io/badge/API-FastAPI-009688)](http://127.0.0.1:8000/docs)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Node](https://img.shields.io/badge/Node-18%2B-green)](https://nodejs.org/)

## 🎬 Overview

Pocket Heist is a **production-ready** web application that allows teams to create, assign, and track playful missions or tasks in a gamified way. The app features a spy-themed dark UI where users can manage active assignments, view archived heists, and create new challenges.

**What makes it special:**
- 🏗️ **API-First Architecture** - Complete backend/frontend separation
- 🔄 **Zero-Backend Migration** - React frontend uses same API as Streamlit (validated)
- 🎨 **Modern UI** - Dark theme with gold accents, toast notifications, skeleton loaders
- 📱 **Fully Responsive** - Mobile-first design with Tailwind CSS
- 🔒 **Secure** - JWT authentication, bcrypt password hashing
- ⚡ **Fast** - Vite dev server, optimized production build (~350KB total)

---

## 📚 Table of Contents

- [Screenshots](#-screenshots)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Getting Started](#-getting-started)
- [Project Structure](#project-structure)
- [API Endpoints](#-api-endpoints)
- [Tech Stack](#tech-stack)
- [Testing](#testing)
- [Deployment](#-deployment)
- [Troubleshooting](#️-troubleshooting)
- [Completed Features](#-completed-features)
- [Roadmap](#️-roadmap)
- [Contributing](#-contributing)
- [Documentation](#-documentation)
- [License](#-license)

---

## 📸 Screenshots

### React Frontend (Phase 2)

**Login Page**
> Dark-themed authentication with spy aesthetic

![Login Page](screenshots\react\login.png)

**War Room - Active Heists**
> Real-time mission tracking with countdown timers

![War Room](screenshots\react\war_room.png)

**My Assignments**
> Track your created heists by status

![My Assignments](screenshots\react\my_assignment.png)

**Blueprint Studio - Create Heist**
> Intuitive form with auto-deadline (+3 hours)

![Create Heist](screenshots\react\new_mission_blueprint.png)

**Intel Archive**
> Browse expired and aborted missions

![Intel Archive](screenshots\react\intel_archive.png)

> 💡 **Tip:** Run the app locally to see the full experience! Follow the Quick Start guide below.

## ✨ Features

### 🔐 Authentication
- **User Registration** - Create account with username and password (min 8 chars)
- **JWT Login** - Secure token-based authentication (24-hour expiry)
- **Protected Routes** - Automatic redirect to login for unauthenticated users
- **Persistent Sessions** - Token stored in localStorage, survives page refresh

### 🎯 Heist Management
- **War Room** - View all active missions with real-time countdown timers
- **My Assignments** - Filter your created heists by status (Active/Expired/Aborted)
- **Blueprint Studio** - Create new heists with auto-deadline (+3 hours)
- **Intel Archive** - Browse historical missions (expired/aborted)
- **Abort Missions** - Creators can abort active heists with confirmation
- **Details Modal** - Full-screen overlay with complete heist information

### 🎨 User Experience (React Frontend)
- **Toast Notifications** - Non-blocking success/error messages with auto-dismiss
- **Skeleton Loaders** - Smooth loading states matching card structure
- **Real-time Search** - Filter heists by title, target, assignee, difficulty
- **Responsive Grid** - 1 column (mobile), 2 columns (tablet), 3 columns (desktop)
- **Smooth Animations** - Fade-ins, slide-ins, hover effects
- **Dark Theme** - Spy-themed UI with `#0a0a0c` background and `#f59e0b` gold accents

## Tech Stack

### Backend
- **Framework**: FastAPI - Modern, fast Python web framework with automatic API documentation
- **Database**: PostgreSQL/SQLite - Relational database for storing heists and user data
- **ORM**: SQLAlchemy - Database abstraction and query builder
- **Authentication**: JWT tokens - Secure stateless authentication
- **Validation**: Pydantic - Data validation using Python type hints

### Frontend
- **Phase 1 - Streamlit**: Rapid prototyping and MVP development
- **Phase 2 - React**: Production-ready, scalable UI ✅ **COMPLETED**
  - React 18 with Vite
  - Tailwind CSS for styling
  - React Router for navigation
  - Axios for API calls
  - Toast notifications and skeleton loaders

### Architecture Approach
The application follows an **API-first architecture** with complete separation between backend and frontend:
- Backend exposes RESTful JSON API endpoints
- All business logic resides in the backend
- Frontend (Streamlit or React) consumes the same API
- No backend changes required when migrating from Streamlit to React
- CORS-enabled API for seamless React integration

## 🚀 Quick Start

**Get the React app running in 3 steps:**

```bash
# 1. Start backend
cd Pocket-Heist
uvicorn backend.main:app --reload

# 2. Start React frontend (new terminal)
cd frontend-react
npm install
npm run dev

# 3. Open browser
# Backend API: http://127.0.0.1:8000/docs
# React App:   http://localhost:5173
```

---

## 📦 Getting Started

### Prerequisites
- **Python 3.10+** - Backend API
- **Node.js 18+** and npm - React frontend
- **Git** - Version control (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Pocket-Heist
   ```

2. **Install backend dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Install Streamlit frontend dependencies (Phase 1)**
   ```bash
   pip install -r frontend/requirements.txt
   ```

4. **Install React frontend dependencies (Phase 2)**
   ```bash
   cd frontend-react
   npm install
   cd ..
   ```

### Running the Application

#### Start the Backend (FastAPI)
```bash
# From project root
uvicorn backend.main:app --reload
```
The API server will start at `http://127.0.0.1:8000`

**API Documentation**: Visit `http://127.0.0.1:8000/docs` for interactive Swagger UI

#### Start the Frontend

**Option 1: Streamlit (Phase 1)**
```bash
# From project root (in a separate terminal)
streamlit run frontend/app.py
```
The Streamlit app will open automatically at `http://localhost:8501`

**Option 2: React (Phase 2 - Recommended)**
```bash
# From frontend-react directory (in a separate terminal)
cd frontend-react
npm run dev
```
The React app will be available at `http://localhost:5173`

For detailed React setup and production build instructions, see [`frontend-react/README.md`](./frontend-react/README.md)

### Testing

**Backend Tests (pytest):**
```bash
# Run all tests
pytest tests/ -v

# Run specific test suites
pytest tests/unit/ -v          # Unit tests
pytest tests/integration/ -v   # Integration tests
pytest tests/smoke/ -v         # API architecture tests

# Run with coverage
pytest --cov=backend tests/
```

**Frontend E2E Tests (Manual):**
```bash
cd frontend-react

# Run API smoke tests (automated)
bash test-api.sh

# Run manual E2E tests
# See: frontend-react/E2E_TEST_CHECKLIST.md
# See: frontend-react/TESTING_GUIDE.md
```

**Note:** Integration tests have known fixture conflicts. Run test suites separately:
```bash
pytest tests/unit/ -v && pytest tests/integration/ -v && pytest tests/smoke/ -v
```

## Project Structure

```
Pocket-Heist/
├── backend/              # FastAPI backend
│   ├── main.py          # FastAPI app entry point
│   ├── database.py      # Database configuration
│   ├── models.py        # SQLAlchemy ORM models
│   ├── schemas.py       # Pydantic schemas
│   ├── auth.py          # JWT authentication
│   ├── user_service.py  # User business logic
│   ├── heist_service.py # Heist business logic
│   ├── dependencies.py  # FastAPI dependencies
│   ├── enums.py         # Enums (Difficulty, HeistStatus)
│   └── routers/         # API route handlers
│       ├── auth.py      # Auth endpoints
│       └── heists.py    # Heist endpoints
├── frontend/            # Streamlit frontend (Phase 1)
│   ├── app.py          # Main Streamlit application
│   └── api_client.py   # Backend API wrapper
├── frontend-react/      # React frontend (Phase 2) ✅
│   ├── src/            # React source code
│   │   ├── components/ # UI components
│   │   ├── contexts/   # React Context providers
│   │   ├── layouts/    # Page layouts
│   │   ├── pages/      # Route pages
│   │   └── services/   # API client
│   ├── dist/           # Production build output
│   └── package.json    # npm dependencies
├── tests/              # Test suite
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── smoke/          # API architecture tests
└── requirements.txt    # Python dependencies
```

## 📡 API Endpoints

**Interactive Documentation:** [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs) (Swagger UI)

### Authentication (Public)

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `POST` | `/auth/register` | Register new user | `{ "username": "string", "password": "string" }` |
| `POST` | `/auth/login` | Login and get JWT | `{ "username": "string", "password": "string" }` |

**Response:** `{ "access_token": "eyJ...", "token_type": "bearer" }`

### Heists (Protected)

All endpoints require: `Authorization: Bearer <jwt_token>`

| Method | Endpoint | Description | Returns |
|--------|----------|-------------|---------|
| `GET` | `/heists` | List all active heists | `Heist[]` |
| `POST` | `/heists` | Create a new heist | `Heist` |
| `GET` | `/heists/{id}` | Get heist by ID | `Heist` |
| `GET` | `/heists/mine` | List user's created heists | `Heist[]` |
| `GET` | `/heists/archive` | List expired/aborted heists | `Heist[]` |
| `PATCH` | `/heists/{id}/abort` | Abort heist (creator only) | `Heist` |

**Heist Schema:**
```json
{
  "id": 1,
  "title": "Operation Coffee Heist",
  "target": "Kitchen Pantry",
  "difficulty": "Medium",
  "assignee_username": "agent_001",
  "creator_username": "admin",
  "deadline": "2026-04-11T15:30:00Z",
  "description": "Secure the last bag of premium coffee beans",
  "status": "Active",
  "created_at": "2026-04-11T12:30:00Z"
}
```

## Development

### Database
The application uses SQLite for development (`pocket_heist.db`). For production, migrate to PostgreSQL by updating the `SQLALCHEMY_DATABASE_URL` in `backend/database.py`.

### Authentication
- JWT tokens expire after 24 hours
- Passwords are hashed using bcrypt
- Stateless authentication (no server-side sessions)

### Testing Philosophy
- **Unit tests**: Test individual functions and business logic
- **Integration tests**: Test API endpoints end-to-end
- **Smoke tests**: Validate API-first architecture requirements
- **Property-based tests**: Use Hypothesis for randomized testing

## 🚢 Deployment

### Production Build (React Frontend)

```bash
cd frontend-react
npm run build
```

**Output:** `dist/` folder (ready for deployment)
- **Bundle size:** ~350 KB (CSS: 18 KB, JS: 332 KB)
- **Optimized:** Minified, tree-shaken, gzip-compressed

### Deploy Frontend

**Static Hosting Options:**
- **Vercel/Netlify** - Deploy `dist/` folder, set `VITE_API_BASE_URL` env var
- **GitHub Pages** - Upload `dist/` contents
- **AWS S3 + CloudFront** - Static website hosting
- **Cloudflare Pages** - Connect Git repository

**Environment Variables:**
```bash
VITE_API_BASE_URL=https://your-backend-api.com
```

### Deploy Backend

**Hosting Options:**
- **Render/Railway** - Python app deployment
- **AWS EC2/Elastic Beanstalk** - Full control
- **Google Cloud Run** - Containerized deployment
- **Heroku** - Simple Python deployment

**Requirements:**
1. Update `SQLALCHEMY_DATABASE_URL` for production database (PostgreSQL)
2. Add production frontend domain to CORS `allow_origins` in `backend/main.py`
3. Set secure JWT secret key (environment variable)
4. Use production-grade WSGI server (Gunicorn + Uvicorn)

**Example production command:**
```bash
gunicorn backend.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 🛠️ Troubleshooting

### Backend Issues

**Problem:** `uvicorn: command not found`
```bash
# Solution: Use python -m uvicorn
python -m uvicorn backend.main:app --reload
```

**Problem:** `ModuleNotFoundError: No module named 'backend'`
```bash
# Solution: Run from project root, not backend/
cd Pocket-Heist  # Not backend/
uvicorn backend.main:app --reload
```

**Problem:** Database errors
```bash
# Solution: Delete database and recreate tables
rm pocket_heist.db
# Restart backend - tables auto-create
```

### Frontend Issues

**Problem:** CORS errors in browser console
```bash
# Solution: Verify backend CORS includes React dev server
# In backend/main.py, check allow_origins includes:
# - http://localhost:5173
# - http://127.0.0.1:5173
```

**Problem:** `VITE_API_BASE_URL` not working
```bash
# Solution: Restart dev server after changing .env
# Vite only reads .env on startup
npm run dev
```

**Problem:** Build errors with Tailwind CSS
```bash
# Solution: Ensure Tailwind v3.4.0 (not v4)
npm uninstall tailwindcss
npm install -D tailwindcss@^3.4.0
```

**Problem:** White screen / React app not loading
```bash
# Solution: Check browser console for errors
# Common issues:
# 1. Backend not running (check http://127.0.0.1:8000)
# 2. Node modules missing (run: npm install)
# 3. Port 5173 in use (kill process or use different port)
```

### Testing Issues

**Problem:** Integration tests fail when run together
```bash
# Solution: Run test suites separately (known fixture issue)
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/smoke/ -v
```

**Problem:** Hypothesis health check warnings
```bash
# Solution: Suppress function_scoped_fixture warnings
# Already configured in tests with:
# @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
```

---

## ✅ Completed Features

### Phase 1: Streamlit Frontend ✅
- Rapid prototyping and MVP development
- API client integration
- Basic authentication flow

### Phase 2: React Frontend ✅ **PRODUCTION-READY**
- ✅ Migrated from Streamlit to React
- ✅ Zero backend changes (API-first architecture validated)
- ✅ Toast notifications and skeleton loaders
- ✅ Modern component-based architecture (React 18)
- ✅ Responsive design with Tailwind CSS
- ✅ Production build optimized (~350 KB)
- ✅ Comprehensive E2E testing documentation

## 🗺️ Roadmap

### Phase 3: Advanced Features (Planned)
- [ ] **Real-time Updates** - WebSocket integration for live heist updates
- [ ] **Comments & Collaboration** - Team discussions on heists
- [ ] **User Profiles** - Stats, badges, achievement system
- [ ] **Advanced Filters** - Date range, difficulty combos, assignee multi-select
- [ ] **Theme Toggle** - Dark/light mode switcher
- [ ] **Notifications** - Browser push notifications for deadlines
- [ ] **File Attachments** - Upload images/docs to heists
- [ ] **Mobile App** - React Native version

### Phase 4: Enterprise Features (Future)
- [ ] **Teams/Organizations** - Multi-tenant support
- [ ] **Permissions & Roles** - Admin, manager, agent roles
- [ ] **Analytics Dashboard** - Success rate, completion times, trends
- [ ] **Integrations** - Slack, Discord, Microsoft Teams webhooks
- [ ] **API Rate Limiting** - Prevent abuse
- [ ] **Audit Logs** - Track all actions for compliance

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Workflow

1. **Fork & Clone**
   ```bash
   git clone https://github.com/your-username/Pocket-Heist.git
   cd Pocket-Heist
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

3. **Make Changes**
   - Follow existing code style (PEP 8 for Python, ESLint for React)
   - Add tests for new features
   - Update documentation (README, CLAUDE.md if architecture changes)

4. **Test Your Changes**
   ```bash
   # Backend tests
   pytest tests/ -v
   
   # Frontend E2E (manual)
   # See: frontend-react/E2E_TEST_CHECKLIST.md
   ```

5. **Commit with Conventional Commits**
   ```bash
   git commit -m "feat: add heist filtering by date range"
   git commit -m "fix: resolve CORS issue with Safari"
   git commit -m "docs: update API endpoint documentation"
   ```

6. **Push & Open PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a Pull Request on GitHub with:
   - Clear description of changes
   - Screenshots/GIFs if UI changes
   - Link to related issues

### Code Guidelines

**Backend (Python):**
- Follow PEP 8 style guide
- Use type hints where possible
- Write docstrings for public functions
- Keep business logic in service files (`heist_service.py`, `user_service.py`)

**Frontend (React):**
- Use functional components with hooks
- Keep components small and focused
- Use Tailwind utility classes (avoid custom CSS)
- Implement loading states with skeletons
- Add error handling with toast notifications

**Database:**
- Never bypass migrations (add new migrations for schema changes)
- Keep `CLAUDE.md` updated if you change route ordering or add new patterns

### What to Contribute

**Good First Issues:**
- Add more heist difficulty levels
- Implement search debouncing
- Add keyboard shortcuts (ESC to close modal)
- Improve error messages
- Add unit tests for React components

**Advanced Features:**
- WebSocket integration for real-time updates
- Comments on heists
- User profile pages
- Advanced filtering UI
- Dark/light theme toggle

---

## 📄 Documentation

- **[CLAUDE.md](./CLAUDE.md)** - Architecture guidance for AI assistants
- **[frontend-react/README.md](./frontend-react/README.md)** - React setup and deployment
- **[frontend-react/E2E_TEST_CHECKLIST.md](./frontend-react/E2E_TEST_CHECKLIST.md)** - Testing guide
- **[API Docs](http://127.0.0.1:8000/docs)** - Interactive Swagger UI (when backend running)

---

## 📞 Support

**Found a bug?** Open an issue with:
- Steps to reproduce
- Expected vs actual behavior
- Browser/OS information
- Console errors (if applicable)

**Have a question?** Check:
1. This README
2. `frontend-react/README.md` for React-specific questions
3. `CLAUDE.md` for architecture decisions
4. API docs at `/docs` endpoint

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **FastAPI** - Modern Python web framework
- **React** - UI library
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide Icons** - Beautiful icon library
- **date-fns** - Date manipulation library

---

## 🌟 Project Stats

- **Backend:** 2,000+ lines of Python code
- **Frontend:** 1,500+ lines of React/JSX code
- **Tests:** 30+ test cases (unit, integration, E2E)
- **API Endpoints:** 8 routes
- **Bundle Size:** ~350 KB (optimized)
- **Development Time:** Phase 1 + Phase 2 completed

---

<div align="center">

**Made with ☕ and 🎯 by the Pocket Heist Team**

[⬆ Back to Top](#pocket-heist-)

</div>
