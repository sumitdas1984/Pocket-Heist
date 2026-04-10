# Implementation Plan: Pocket Heist

## Overview

Implement the Pocket Heist application incrementally: start with the FastAPI project skeleton and database models, then build auth, then heist CRUD, then the Streamlit frontend. Each phase wires into the previous one so there is no orphaned code.

## Tasks

- [ ] 1. Set up project structure, dependencies, and database foundation
  - Create directory layout: `backend/`, `frontend/`, `tests/unit/`, `tests/integration/`, `tests/smoke/`
  - Create `backend/requirements.txt` with: fastapi, uvicorn, sqlalchemy, pydantic, python-jose[cryptography], passlib[bcrypt], hypothesis, pytest, httpx
  - Create `frontend/requirements.txt` with: streamlit, requests, pandas
  - Create `backend/database.py` with SQLAlchemy engine, `SessionLocal`, and `Base`
  - Create `backend/models.py` with `User` and `Heist` ORM models (all fields per design)
  - Create `backend/enums.py` with `Difficulty` and `HeistStatus` enums
  - Create `backend/main.py` with a bare FastAPI app, CORS middleware configured for localhost origins, and `Base.metadata.create_all()` on startup
  - _Requirements: 12.1, 12.2_

- [ ] 2. Implement Pydantic schemas and validators
  - [ ] 2.1 Create `backend/schemas.py` with all Pydantic models: `UserCreate`, `UserResponse`, `TokenResponse`, `HeistCreate` (with future-deadline validator), `HeistResponse`
    - _Requirements: 1.3, 1.4, 4.2, 4.3, 4.4, 11.1, 11.2, 11.3_

  - [ ]* 2.2 Write property test for short password rejection (Property 3)
    - **Property 3: Short password rejection**
    - **Validates: Requirements 1.3**
    - File: `tests/unit/test_validators.py`

  - [ ]* 2.3 Write property test for invalid difficulty rejection (Property 9)
    - **Property 9: Invalid difficulty values are rejected**
    - **Validates: Requirements 4.3**
    - File: `tests/unit/test_validators.py`

  - [ ]* 2.4 Write property test for past deadline rejection (Property 10)
    - **Property 10: Past deadline is rejected**
    - **Validates: Requirements 4.4**
    - File: `tests/unit/test_validators.py`

  - [ ]* 2.5 Write property test for HeistResponse serialization round-trip (Property 19)
    - **Property 19: Heist serialization round-trip**
    - **Validates: Requirements 11.4**
    - File: `tests/unit/test_validators.py`

- [ ] 3. Implement user service and auth endpoints
  - [ ] 3.1 Create `backend/auth.py` with JWT creation/decoding helpers (24-hour expiry, HS256)
    - _Requirements: 2.4, 2.5, 2.7_

  - [ ]* 3.2 Write property test for JWT round-trip (Property 4)
    - **Property 4: Login round-trip produces a valid JWT**
    - **Validates: Requirements 2.1, 2.4**
    - File: `tests/unit/test_auth.py`

  - [ ] 3.3 Create `backend/user_service.py` with `register_user()` (bcrypt hash, duplicate check) and `authenticate_user()` (verify hash, return JWT)
    - _Requirements: 1.1, 1.2, 1.5, 2.1, 2.2, 2.3_

  - [ ] 3.4 Create `backend/routers/auth.py` with `POST /auth/register` and `POST /auth/login` endpoints; mount router in `main.py`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3_

  - [ ]* 3.5 Write property test for password hashing invariant (Property 1)
    - **Property 1: Password hashing invariant**
    - **Validates: Requirements 1.5**
    - File: `tests/integration/test_auth_api.py`

  - [ ]* 3.6 Write property test for duplicate username rejection (Property 2)
    - **Property 2: Duplicate username rejection**
    - **Validates: Requirements 1.2**
    - File: `tests/integration/test_auth_api.py`

  - [ ]* 3.7 Write property test for wrong-password login rejection (Property 5)
    - **Property 5: Wrong-password login is rejected**
    - **Validates: Requirements 2.2**
    - File: `tests/integration/test_auth_api.py`

  - [ ]* 3.8 Write property test for unregistered username login rejection (Property 6)
    - **Property 6: Unregistered username login is rejected**
    - **Validates: Requirements 2.3**
    - File: `tests/integration/test_auth_api.py`

- [ ] 4. Checkpoint — Ensure all auth tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implement JWT dependency and protected route enforcement
  - [ ] 5.1 Add `get_current_user` FastAPI dependency in `backend/dependencies.py` that validates the Bearer token and returns the current `User`; return 401 on missing/invalid/expired token
    - _Requirements: 2.5, 2.6, 2.7, 3.1_

  - [ ]* 5.2 Write property test for all heist endpoints requiring authentication (Property 7)
    - **Property 7: All heist endpoints require authentication**
    - **Validates: Requirements 2.6, 3.1**
    - File: `tests/integration/test_auth_api.py`

- [ ] 6. Implement heist service and CRUD endpoints
  - [ ] 6.1 Create `backend/heist_service.py` with all service functions: `create_heist`, `list_active_heists` (deadline-aware filter), `list_archive_heists`, `list_my_heists`, `get_heist`, `abort_heist`
    - _Requirements: 4.1, 4.5, 4.6, 5.1, 5.2, 6.1, 6.2, 7.1, 7.2, 8.1, 8.2, 9.1, 9.2, 9.3, 9.4, 10.1, 10.2_

  - [ ]* 6.2 Write property test for heist creation sets creator and Active status (Property 8)
    - **Property 8: Heist creation sets creator and Active status**
    - **Validates: Requirements 4.5, 4.6**
    - File: `tests/unit/test_heist_service.py`

  - [ ]* 6.3 Write property test for active heist list excludes past-deadline heists (Property 11)
    - **Property 11: Active heist list excludes past-deadline heists**
    - **Validates: Requirements 5.1, 10.1, 10.2**
    - File: `tests/unit/test_heist_service.py`

  - [ ]* 6.4 Write property test for archive list contains only Expired or Aborted heists (Property 12)
    - **Property 12: Archive list contains only Expired or Aborted heists**
    - **Validates: Requirements 7.1**
    - File: `tests/unit/test_heist_service.py`

  - [ ]* 6.5 Write property test for my-heists list contains only requesting user's heists (Property 13)
    - **Property 13: My-heists list contains only the requesting user's heists**
    - **Validates: Requirements 6.1**
    - File: `tests/unit/test_heist_service.py`

  - [ ]* 6.6 Write property test for abort by non-creator is forbidden (Property 16)
    - **Property 16: Abort by non-creator is forbidden**
    - **Validates: Requirements 9.2**
    - File: `tests/unit/test_heist_service.py`

  - [ ]* 6.7 Write property test for abort transitions Active heist to Aborted (Property 17)
    - **Property 17: Abort transitions Active heist to Aborted**
    - **Validates: Requirements 9.1**
    - File: `tests/unit/test_heist_service.py`

  - [ ]* 6.8 Write property test for aborting a non-Active heist returns 409 (Property 18)
    - **Property 18: Aborting a non-Active heist returns 409**
    - **Validates: Requirements 9.3**
    - File: `tests/unit/test_heist_service.py`

- [ ] 7. Implement heist API router and wire into app
  - [ ] 7.1 Create `backend/routers/heists.py` with all heist endpoints: `GET /heists`, `POST /heists`, `GET /heists/archive`, `GET /heists/mine`, `GET /heists/{id}`, `PATCH /heists/{id}/abort`; mount router in `main.py`
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 6.1, 6.2, 7.1, 7.2, 8.1, 8.2, 9.1, 9.2, 9.3, 9.4_

  - [ ]* 7.2 Write property test for heist retrieval round-trip (Property 14)
    - **Property 14: Heist retrieval round-trip**
    - **Validates: Requirements 8.1**
    - File: `tests/integration/test_heist_api.py`

  - [ ]* 7.3 Write property test for non-existent heist retrieval returns 404 (Property 15)
    - **Property 15: Non-existent heist retrieval returns 404**
    - **Validates: Requirements 8.2**
    - File: `tests/integration/test_heist_api.py`

- [ ] 8. Checkpoint — Ensure all backend tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 9. Add smoke tests for API-first architecture requirements
  - [ ] 9.1 Create `tests/smoke/test_api_setup.py` with tests for `/docs` accessibility, CORS headers on heist endpoints, and JSON `content-type` on all list endpoints
    - _Requirements: 12.1, 12.2, 12.3_

- [ ] 10. Implement Streamlit frontend
  - [ ] 10.1 Create `frontend/api_client.py` with helper functions wrapping all backend API calls (register, login, list heists, create heist, abort heist, get archive, get mine) using the `requests` library; store JWT in `st.session_state`
    - _Requirements: 3.2, 3.3, 12.1_

  - [ ] 10.2 Create `frontend/app.py` with the login screen: centered layout, "Establish Connection" header, operative codename + encryption key fields, "Authenticate" button; on failure show `st.error("Invalid credentials.")`; on success store token and rerun
    - _Requirements: 2.1, 2.2, 3.2_

  - [ ] 10.3 Add sidebar navigation (War Room | Mission Archive | Plan New Heist | Terminate Session) and unauthenticated redirect to login
    - _Requirements: 3.2, 3.3_

  - [ ] 10.4 Implement War Room view: fetch active heists from `GET /heists`, render 2-column card grid with gold-border heist cards (title, target, difficulty, assignee, deadline, IN PROGRESS badge), and per-card "Abort" button calling `PATCH /heists/{id}/abort`
    - _Requirements: 5.1, 5.2, 5.3, 9.1_

  - [ ] 10.5 Implement Mission Archive view: fetch from `GET /heists/archive`, render with `st.table` showing all heist fields
    - _Requirements: 7.1, 7.2, 7.3_

  - [ ] 10.6 Implement Plan New Heist form: Mission Name, Target, Difficulty selectbox, Assign to Operative, Intel/Mission Details textarea; deadline auto-set to +3 hours; on submit call `POST /heists`; show `st.warning("Blueprint incomplete. Fill all required fields.")` on validation error
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

  - [ ] 10.7 Apply dark terminal CSS theme (`#0e1117` background, `#ffd700` gold accents, matrix-green status badge) matching the UI mockup
    - _Requirements: 5.3_

- [ ] 11. Final checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

---

## Phase 2: React Frontend Migration

### Prerequisites
- Phase 1 (Streamlit frontend) completed
- Backend API fully functional and tested
- React UI mockup reviewed (`ui-mockup/react/App.jsx`)

### Tasks

- [ ] 12. Set up React project structure and dependencies
  - [ ] 12.1 Initialize React project with Vite in `frontend-react/` directory
    - Use: `npm create vite@latest frontend-react -- --template react`
  
  - [ ] 12.2 Install core dependencies
    - React Router DOM for navigation
    - Axios or Fetch API wrapper for HTTP requests
    - Tailwind CSS for styling
    - Lucide React for icons (matching mockup)
    - date-fns or dayjs for date formatting
  
  - [ ] 12.3 Configure Tailwind CSS with dark theme
    - Extend theme with custom colors: `#0a0a0c` background, `amber-500` primary
    - Configure background gradients matching mockup
  
  - [ ] 12.4 Set up environment variables
    - Create `.env` file with `VITE_API_BASE_URL=http://127.0.0.1:8000`
    - Add `.env` to `.gitignore`

- [ ] 13. Implement API client layer
  - [ ] 13.1 Create `src/services/api.js` with Axios instance
    - Base URL from environment variable
    - Request interceptor to add `Authorization: Bearer <token>` header
    - Response interceptor for error handling (401 → logout, etc.)
  
  - [ ] 13.2 Create `src/services/auth.js` with authentication functions
    - `register(username, password)` → POST `/auth/register`
    - `login(username, password)` → POST `/auth/login`, store JWT in localStorage
    - `logout()` → clear localStorage and redirect
    - `getToken()` → retrieve JWT from localStorage
    - `isAuthenticated()` → check if valid token exists
  
  - [ ] 13.3 Create `src/services/heists.js` with heist management functions
    - `listActiveHeists()` → GET `/heists`
    - `listMyHeists()` → GET `/heists/mine`
    - `listArchiveHeists()` → GET `/heists/archive`
    - `getHeist(id)` → GET `/heists/{id}`
    - `createHeist(data)` → POST `/heists`
    - `abortHeist(id)` → PATCH `/heists/{id}/abort`

- [ ] 14. Implement authentication and routing
  - [ ] 14.1 Create `src/contexts/AuthContext.jsx` for auth state management
    - Provide: `user`, `token`, `login()`, `logout()`, `isAuthenticated`
    - Persist auth state across page refreshes using localStorage
  
  - [ ] 14.2 Create `src/components/ProtectedRoute.jsx` component
    - Redirect to `/login` if not authenticated
    - Render children if authenticated
  
  - [ ] 14.3 Set up React Router in `src/App.jsx`
    - Route: `/login` → LandingPage (public)
    - Route: `/` → Dashboard (protected)
    - Route: `/war-room` → War Room view (protected)
    - Route: `/my-assignments` → My Assignments view (protected)
    - Route: `/create` → Blueprint Studio (protected)
    - Route: `/archive` → Intel Archive (protected)
    - Default redirect: `/` → `/war-room` (when authenticated)

- [ ] 15. Implement LandingPage (Login/Register)
  - [ ] 15.1 Create `src/pages/LandingPage.jsx` matching mockup design
    - Centered card layout with Shield icon
    - "POCKET HEIST" title with italic font
    - Login form: Operative Codename + Access Credentials
    - "Establish Connection" button
    - "Apply for New Credentials" link for registration
    - Background decorative elements (amber/blue blur circles)
  
  - [ ] 15.2 Add form validation
    - Required fields
    - Password minimum 8 characters
    - Display error messages on failed login
  
  - [ ] 15.3 Implement registration modal/flow
    - Toggle between login and register forms
    - Call `auth.register()` on submit
    - Show success message, switch to login form

- [ ] 16. Implement Dashboard layout and sidebar
  - [ ] 16.1 Create `src/layouts/DashboardLayout.jsx`
    - Sidebar with "POCKET HEIST" branding (Shield icon)
    - Navigation menu: War Room, My Assignments, Blueprint Studio, Intel Archive
    - Active tab highlighting (amber-500 background, black text)
    - User profile card at bottom (avatar, name, rank)
    - Logout button
  
  - [ ] 16.2 Create `src/components/NavItem.jsx`
    - Icon + label
    - Active/inactive states
    - Hover effects
  
  - [ ] 16.3 Implement main content area
    - Header with page title and search bar
    - Filter button
    - Content outlet for nested routes

- [ ] 17. Implement War Room view (Active Heists)
  - [ ] 17.1 Create `src/pages/WarRoom.jsx`
    - Fetch active heists on mount using `heists.listActiveHeists()`
    - Display loading state while fetching
    - Show empty state if no active heists
  
  - [ ] 17.2 Create `src/components/HeistCard.jsx`
    - Match mockup design: dark card, gold border on hover
    - Status badge (Active → green, Completed → blue, Expired → rose)
    - Heist ID badge (#0001 format)
    - Title, description (2-line clamp)
    - Info rows: Target, Difficulty, Operative, Time Remaining
    - "View Intel" button
    - "Abort" button (only if user is creator and status is Active)
  
  - [ ] 17.3 Implement HeistGrid layout
    - Responsive grid: 1 column (mobile), 2 columns (tablet), 3 columns (desktop)
    - Grid gap for spacing

- [ ] 18. Implement My Assignments view
  - [ ] 18.1 Create `src/pages/MyAssignments.jsx`
    - Fetch heists created by current user using `heists.listMyHeists()`
    - Reuse `HeistCard` and `HeistGrid` components
    - Show all statuses (Active, Expired, Aborted)

- [ ] 19. Implement Blueprint Studio (Create Heist)
  - [ ] 19.1 Create `src/pages/BlueprintStudio.jsx`
    - Form card matching mockup design
    - Icon header with PlusSquare icon
    - "Create Mission Blueprint" title
  
  - [ ] 19.2 Create form with fields
    - Mission Name (text input)
    - Target Sector (text input)
    - Difficulty (select: Training, Easy, Medium, Hard, Legendary)
    - Assign Operative (text input - assignee username)
    - Intel Briefing (textarea)
    - Auto-set deadline to +3 hours from current time
  
  - [ ] 19.3 Implement form submission
    - Validate all required fields
    - Call `heists.createHeist(data)`
    - Show success toast/notification
    - Reset form
    - Redirect to War Room or stay on form

- [ ] 20. Implement Intel Archive (Archived Heists)
  - [ ] 20.1 Create `src/pages/IntelArchive.jsx`
    - Fetch expired/aborted heists using `heists.listArchiveHeists()`
    - Reuse `HeistCard` and `HeistGrid` components
    - Display only Expired and Aborted status heists
  
  - [ ] 20.2 Add filtering/sorting options
    - Filter by status (Expired, Aborted, All)
    - Sort by deadline, created date

- [ ] 21. Implement Heist Details modal/page (optional enhancement)
  - [ ] 21.1 Create `src/components/HeistDetailsModal.jsx`
    - Show full heist information
    - Display all fields including description
    - "View Intel" button in HeistCard opens this modal
  
  - [ ] 21.2 Add abort functionality in modal
    - Abort button for creators
    - Confirmation dialog before aborting

- [ ] 22. Add UI polish and UX improvements
  - [ ] 22.1 Implement loading states
    - Skeleton loaders for heist cards while fetching
    - Loading spinner for form submissions
  
  - [ ] 22.2 Implement error handling
    - Toast notifications for errors
    - Retry buttons for failed requests
  
  - [ ] 22.3 Add animations and transitions
    - Page transitions
    - Card hover effects (shadow, border glow)
    - Button hover states
  
  - [ ] 22.4 Implement search functionality (header search bar)
    - Filter heists by title or target
    - Real-time search as user types

- [ ] 23. Configure build and deployment
  - [ ] 23.1 Update CORS in backend
    - Add React dev server URL to allowed origins
    - Add production domain when deployed
  
  - [ ] 23.2 Create production build
    - Run `npm run build`
    - Test production build locally with `npm run preview`
  
  - [ ] 23.3 Update README with React setup instructions
    - Installation steps
    - Development server commands
    - Environment variable configuration

- [ ] 24. Final checkpoint — Test React frontend end-to-end
  - [ ] 24.1 Test authentication flow
    - Register new user
    - Login with credentials
    - Logout and verify redirect
  
  - [ ] 24.2 Test heist management
    - Create new heist
    - View in War Room
    - View in My Assignments
    - Abort heist
    - Verify appears in Archive
  
  - [ ] 24.3 Test cross-browser compatibility
    - Chrome, Firefox, Safari, Edge
  
  - [ ] 24.4 Test responsive design
    - Mobile, tablet, desktop breakpoints

## Notes

### Phase 1 (Streamlit)
- Tasks marked with `*` are optional and can be skipped for a faster MVP
- Each task references specific requirements for traceability
- Property tests use `hypothesis` and must include the comment `# Feature: pocket-heist, Property N: <title>`
- The `/heists/archive` route must be registered before `/heists/{id}` in the router to avoid FastAPI treating "archive" as an integer path parameter
- The deadline-aware active heist filter (`deadline > now()`) is applied at query time in `list_active_heists`; no background scheduler is needed for Phase 1

### Phase 2 (React)
- Backend API remains unchanged throughout React migration
- JWT tokens stored in `localStorage` (replace Streamlit's `st.session_state`)
- All API calls use Axios with automatic token injection
- React mockup exists in `ui-mockup/react/App.jsx` as design reference
- Use Vite for faster development and build times
- Tailwind CSS for styling (matching dark theme: `#0a0a0c`, `amber-500`)
- Lucide React for icons (Shield, Map, Zap, PlusSquare, Clock, etc.)
