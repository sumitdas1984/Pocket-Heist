"""
Simplified integration tests for quick validation
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app
from backend.database import Base, get_db
from backend.models import User

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_simple.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    """Setup and teardown database for each test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


def test_user_registration_hashes_password(client):
    """Test that password is hashed when stored"""
    username = "testuser"
    password = "testpass123"

    # Register user
    response = client.post(
        "/auth/register",
        json={"username": username, "password": password}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == username
    assert "password" not in data
    assert "hashed_password" not in data

    # Check password is hashed in database
    db = TestingSessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        assert user is not None
        assert user.hashed_password != password
        assert user.hashed_password.startswith("$2b$")  # bcrypt hash starts with this
    finally:
        db.close()


def test_duplicate_username_returns_409(client):
    """Test that duplicate usernames are rejected"""
    username = "duplicate"

    # First registration
    response1 = client.post(
        "/auth/register",
        json={"username": username, "password": "password123"}
    )
    assert response1.status_code == 201

    # Second registration with same username
    response2 = client.post(
        "/auth/register",
        json={"username": username, "password": "different456"}
    )
    assert response2.status_code == 409


def test_successful_login_returns_token(client):
    """Test that valid credentials return a JWT token"""
    username = "loginuser"
    password = "loginpass123"

    # Register
    client.post(
        "/auth/register",
        json={"username": username, "password": password}
    )

    # Login
    response = client.post(
        "/auth/login",
        params={"username": username, "password": password}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0


def test_wrong_password_returns_401(client):
    """Test that wrong password is rejected"""
    username = "wrongpass"
    correct_password = "correct123"
    wrong_password = "wrong123"

    # Register
    client.post(
        "/auth/register",
        json={"username": username, "password": correct_password}
    )

    # Login with wrong password
    response = client.post(
        "/auth/login",
        params={"username": username, "password": wrong_password}
    )

    assert response.status_code == 401


def test_unregistered_user_login_returns_401(client):
    """Test that unregistered user cannot login"""
    response = client.post(
        "/auth/login",
        params={"username": "nonexistent", "password": "password123"}
    )

    assert response.status_code == 401


def test_short_password_returns_422(client):
    """Test that passwords shorter than 8 characters are rejected"""
    response = client.post(
        "/auth/register",
        json={"username": "shortpass", "password": "short"}
    )

    assert response.status_code == 422
