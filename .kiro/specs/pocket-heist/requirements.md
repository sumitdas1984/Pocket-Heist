# Requirements Document

## Introduction

Pocket Heist is a gamified task assignment web application where teams create, assign, and track playful missions ("heists") with a spy/heist-themed interface. The system follows an API-first architecture: a FastAPI backend exposes RESTful JSON endpoints consumed by a Streamlit frontend (Phase 1), with a future React migration path (Phase 2). Users authenticate via JWT tokens and can manage heists across active, assigned, and expired states.

## Glossary

- **System**: The Pocket Heist application as a whole
- **API**: The FastAPI backend service exposing RESTful JSON endpoints
- **Frontend**: The Streamlit (Phase 1) or React (Phase 2) user interface
- **User**: An authenticated person with a registered account
- **Heist**: A gamified task or mission with a title, target, difficulty, assignee, deadline, description, and status
- **Creator**: The User who created a given Heist
- **Assignee**: The User to whom a Heist is assigned
- **JWT**: JSON Web Token used for stateless authentication
- **Active Heist**: A Heist whose deadline has not yet passed and has not been aborted
- **Expired Heist**: A Heist whose deadline has passed
- **Aborted Heist**: A Heist that was manually cancelled before its deadline
- **War Room**: The dashboard view showing all Active Heists
- **Mission Archive**: The dashboard view showing Expired and Aborted Heists
- **Difficulty**: A categorical rating for a Heist — one of: Training, Easy, Medium, Hard, Legendary
- **Validator**: The Pydantic-based input validation layer in the API

---

## Requirements

### Requirement 1: User Registration

**User Story:** As a new user, I want to create an account, so that I can access the Pocket Heist dashboard and start planning heists.

#### Acceptance Criteria

1. WHEN a registration request is received with a unique username and a password of at least 8 characters, THE API SHALL create a new User account and return a 201 status code.
2. WHEN a registration request is received with a username that already exists, THE API SHALL return a 409 status code with a descriptive error message.
3. WHEN a registration request is received with a password shorter than 8 characters, THE Validator SHALL return a 422 status code with a descriptive validation error.
4. WHEN a registration request is received with a missing username or missing password field, THE Validator SHALL return a 422 status code with a descriptive validation error.
5. THE API SHALL store passwords as hashed values using a one-way cryptographic hash; plaintext passwords SHALL NOT be persisted.

---

### Requirement 2: User Authentication

**User Story:** As a registered user, I want to log in with my credentials, so that I can receive a token and access protected features.

#### Acceptance Criteria

1. WHEN a login request is received with a valid username and correct password, THE API SHALL return a JWT access token and a 200 status code.
2. WHEN a login request is received with a valid username and incorrect password, THE API SHALL return a 401 status code with a descriptive error message.
3. WHEN a login request is received with a username that does not exist, THE API SHALL return a 401 status code with a descriptive error message.
4. THE API SHALL issue JWT tokens with an expiry of no more than 24 hours.
5. WHILE a JWT token is valid and unexpired, THE API SHALL accept it as proof of authentication on protected endpoints.
6. WHEN a request to a protected endpoint is received without a JWT token, THE API SHALL return a 401 status code.
7. WHEN a request to a protected endpoint is received with an expired or invalid JWT token, THE API SHALL return a 401 status code.

---

### Requirement 3: Protected Route Enforcement

**User Story:** As a system operator, I want dashboard pages to be accessible only to authenticated users, so that heist data is not exposed to unauthenticated visitors.

#### Acceptance Criteria

1. WHEN an unauthenticated request is made to any heist management endpoint, THE API SHALL return a 401 status code.
2. WHEN an unauthenticated user navigates to a dashboard page in the Frontend, THE Frontend SHALL redirect the user to the login page.
3. WHILE a user is authenticated, THE Frontend SHALL display the full dashboard navigation including War Room, Mission Archive, and Plan New Heist sections.

---

### Requirement 4: Create a Heist

**User Story:** As an authenticated user, I want to create a new heist with custom details, so that I can assign missions to other operatives.

#### Acceptance Criteria

1. WHEN a create-heist request is received with a title, target, difficulty, assignee username, and deadline, THE API SHALL persist the Heist and return a 201 status code with the created Heist object.
2. WHEN a create-heist request is received with a missing required field (title, target, difficulty, assignee, or deadline), THE Validator SHALL return a 422 status code with a descriptive validation error identifying the missing field.
3. WHEN a create-heist request is received with a difficulty value not in [Training, Easy, Medium, Hard, Legendary], THE Validator SHALL return a 422 status code with a descriptive validation error.
4. WHEN a create-heist request is received with a deadline that is in the past, THE Validator SHALL return a 422 status code with a descriptive validation error.
5. THE API SHALL record the authenticated User as the Creator of the newly created Heist.
6. THE API SHALL set the initial status of a newly created Heist to Active.

---

### Requirement 5: View Active Heists (War Room)

**User Story:** As an authenticated user, I want to view all active heists, so that I can track ongoing missions across the team.

#### Acceptance Criteria

1. WHEN a request to list active heists is received, THE API SHALL return all Heists with status Active, each including title, target, difficulty, assignee, creator, deadline, and status fields.
2. WHEN no Active Heists exist, THE API SHALL return an empty list with a 200 status code.
3. THE Frontend SHALL display Active Heists in the War Room view as individual heist cards showing title, target, difficulty, assignee, and deadline.

---

### Requirement 6: View Assigned Heists

**User Story:** As an authenticated user, I want to see the heists I have created and assigned to others, so that I can monitor missions I am responsible for.

#### Acceptance Criteria

1. WHEN a request to list assigned heists is received, THE API SHALL return all Heists where the Creator matches the authenticated User, including heists of any status.
2. WHEN the authenticated User has no created Heists, THE API SHALL return an empty list with a 200 status code.

---

### Requirement 7: View Expired Heists (Mission Archive)

**User Story:** As an authenticated user, I want to browse historical missions, so that I can review past heist activity.

#### Acceptance Criteria

1. WHEN a request to list expired heists is received, THE API SHALL return all Heists with status Expired or Aborted, each including all Heist fields.
2. WHEN no Expired or Aborted Heists exist, THE API SHALL return an empty list with a 200 status code.
3. THE Frontend SHALL display Expired and Aborted Heists in the Mission Archive view in a tabular format.

---

### Requirement 8: View Heist Details

**User Story:** As an authenticated user, I want to view comprehensive information about a specific heist, so that I can understand the full mission brief.

#### Acceptance Criteria

1. WHEN a request to retrieve a Heist by its identifier is received and the Heist exists, THE API SHALL return the full Heist object including title, target, difficulty, assignee, creator, deadline, description, and status with a 200 status code.
2. WHEN a request to retrieve a Heist by its identifier is received and the Heist does not exist, THE API SHALL return a 404 status code with a descriptive error message.

---

### Requirement 9: Abort a Heist

**User Story:** As an authenticated user, I want to abort an active heist, so that I can cancel missions that are no longer relevant.

#### Acceptance Criteria

1. WHEN an abort request is received for an Active Heist and the authenticated User is the Creator of that Heist, THE API SHALL set the Heist status to Aborted and return a 200 status code.
2. WHEN an abort request is received for a Heist and the authenticated User is not the Creator of that Heist, THE API SHALL return a 403 status code with a descriptive error message.
3. WHEN an abort request is received for a Heist that is already Expired or Aborted, THE API SHALL return a 409 status code with a descriptive error message.
4. WHEN an abort request is received for a Heist identifier that does not exist, THE API SHALL return a 404 status code with a descriptive error message.

---

### Requirement 10: Automatic Heist Expiry

**User Story:** As a user, I want heists to automatically transition to expired status when their deadline passes, so that the War Room only shows genuinely active missions.

#### Acceptance Criteria

1. WHEN the current time exceeds a Heist's deadline and the Heist status is Active, THE System SHALL transition the Heist status to Expired.
2. WHEN a request to list Active Heists is received, THE API SHALL exclude any Heist whose deadline has passed, regardless of whether a background process has updated its status.

---

### Requirement 11: Heist Data Validation and Serialization

**User Story:** As a developer, I want all heist data to be validated on input and consistently serialized on output, so that the API contract is reliable and the frontend can depend on a stable data shape.

#### Acceptance Criteria

1. THE Validator SHALL validate all incoming Heist creation and update payloads against the defined Heist schema before any persistence operation.
2. WHEN an invalid payload is received, THE Validator SHALL return a 422 status code with a structured error response identifying each invalid field and the reason for rejection.
3. THE API SHALL serialize all Heist responses as JSON objects conforming to the defined Heist schema.
4. FOR ALL valid Heist objects, serializing to JSON and then deserializing back to a Heist object SHALL produce an equivalent Heist object (round-trip property).

---

### Requirement 12: API-First Architecture and CORS

**User Story:** As a developer, I want the backend API to be fully decoupled from the frontend, so that the Streamlit frontend can be replaced with a React frontend without any backend changes.

#### Acceptance Criteria

1. THE API SHALL expose all functionality exclusively through RESTful JSON endpoints; no server-side HTML rendering SHALL be performed by the API.
2. THE API SHALL include CORS headers permitting requests from configured frontend origins, so that a browser-based React frontend can consume the API.
3. THE API SHALL provide auto-generated interactive documentation (e.g., OpenAPI/Swagger) accessible at a dedicated endpoint.
4. WHERE a React frontend is deployed, THE API SHALL serve it without requiring any modification to API endpoint logic or data contracts.
