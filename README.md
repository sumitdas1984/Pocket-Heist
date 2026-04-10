# Pocket Heist

A fun, gamified task assignment application where users create and manage "heists" - tiny missions with big office mischief potential.

## Overview

Pocket Heist is a web application that allows teams to create, assign, and track playful missions or tasks in a gamified way. The app features a heist-themed interface where users can manage active assignments, view expired heists, and create new challenges.

## Features

### Authentication
- **User Sign Up** - Create a new account to start planning heists
- **User Login** - Secure access to your heist dashboard
- **Protected Routes** - Dashboard pages are accessible only to authenticated users

### Heist Management
- **View Active Heists** - Track your ongoing missions and assignments
- **Assigned Heists** - See heists you've created and assigned to others
- **Expired Heists** - Browse historical missions that have completed
- **Create New Heists** - Design and launch new missions with custom details
- **Heist Details** - View comprehensive information about individual heists

### User Interface
- **Responsive Design** - Modern, mobile-friendly layouts
- **Intuitive Navigation** - Easy app navigation with clear sections
- **Organized Layout** - Separate public and authenticated user areas

## Tech Stack

### Backend
- **Framework**: FastAPI - Modern, fast Python web framework with automatic API documentation
- **Database**: PostgreSQL/SQLite - Relational database for storing heists and user data
- **ORM**: SQLAlchemy - Database abstraction and query builder
- **Authentication**: JWT tokens - Secure stateless authentication
- **Validation**: Pydantic - Data validation using Python type hints

### Frontend
- **Phase 1 - Streamlit**: Rapid prototyping and MVP development
- **Phase 2 - React**: Production-ready, scalable UI (future migration)

### Architecture Approach
The application follows an **API-first architecture** with complete separation between backend and frontend:
- Backend exposes RESTful JSON API endpoints
- All business logic resides in the backend
- Frontend (Streamlit or React) consumes the same API
- No backend changes required when migrating from Streamlit to React
- CORS-enabled API for seamless React integration

## Getting Started

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

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

3. **Install frontend dependencies**
   ```bash
   pip install -r frontend/requirements.txt
   ```

### Running the Application

#### Start the Backend (FastAPI)
```bash
# From project root
uvicorn backend.main:app --reload
```
The API server will start at `http://127.0.0.1:8000`

**API Documentation**: Visit `http://127.0.0.1:8000/docs` for interactive Swagger UI

#### Start the Frontend (Streamlit)
```bash
# From project root (in a separate terminal)
streamlit run frontend/app.py
```
The Streamlit app will open automatically at `http://localhost:8501`

### Testing

Run all tests:
```bash
pytest tests/ -v
```

Run specific test suites:
```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# Smoke tests (API architecture validation)
pytest tests/smoke/ -v
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
├── frontend/            # Streamlit frontend
│   ├── app.py          # Main Streamlit application
│   └── api_client.py   # Backend API wrapper
├── tests/              # Test suite
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── smoke/          # API architecture tests
└── requirements.txt    # Python dependencies
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token

### Heists
- `GET /heists` - List all active heists
- `POST /heists` - Create a new heist
- `GET /heists/{id}` - Get heist details
- `GET /heists/archive` - List expired/aborted heists
- `GET /heists/mine` - List heists created by current user
- `PATCH /heists/{id}/abort` - Abort a heist (creator only)

All heist endpoints require JWT authentication via `Authorization: Bearer <token>` header.

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

## Future Roadmap

### Phase 2: React Frontend
- Migrate from Streamlit to React for production UI
- No backend changes required (API-first architecture)
- Enhanced user experience and performance
- Modern component-based architecture

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.
