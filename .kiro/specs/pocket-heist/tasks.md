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

## Notes

- Tasks marked with `*` are optional and can be skipped for a faster MVP
- Each task references specific requirements for traceability
- Property tests use `hypothesis` and must include the comment `# Feature: pocket-heist, Property N: <title>`
- The `/heists/archive` route must be registered before `/heists/{id}` in the router to avoid FastAPI treating "archive" as an integer path parameter
- The deadline-aware active heist filter (`deadline > now()`) is applied at query time in `list_active_heists`; no background scheduler is needed for Phase 1
