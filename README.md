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
