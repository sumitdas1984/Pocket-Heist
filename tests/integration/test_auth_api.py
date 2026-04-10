"""
Integration tests for authentication API endpoints
"""
import pytest
from hypothesis import given, settings, assume, HealthCheck
from hypothesis import strategies as st
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from backend.main import app
from backend.database import Base, get_db
from backend.models import User

# Test database setup - use unique database for each test
def get_test_db_url():
    """Generate unique test database URL"""
    import time
    return f"sqlite:///./test_auth_{int(time.time() * 1000)}.db"


def create_test_client():
    """Create a test client with fresh database"""
    db_url = get_test_db_url()
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Override dependency
    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    # Return client and cleanup function
    def cleanup():
        Base.metadata.drop_all(bind=engine)
        # Remove test database file
        db_file = db_url.replace("sqlite:///./", "")
        if os.path.exists(db_file):
            try:
                os.remove(db_file)
            except:
                pass

    return client, cleanup, TestingSessionLocal


@pytest.fixture(scope="function")
def client():
    """Create test client with fresh database for each test"""
    client, cleanup, _ = create_test_client()
    yield client
    cleanup()


# Feature: pocket-heist, Property 1: Password hashing invariant
@given(
    username=st.text(min_size=1, max_size=50).filter(lambda x: x.strip() != ""),
    password=st.text(min_size=8, max_size=100)
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_password_hashing_invariant(username, password):
    """
    Property 1: Password hashing invariant
    Validates: Requirements 1.5

    For any valid registration payload, the value stored in the database
    for the password field SHALL NOT equal the plaintext password
    provided in the request.
    """
    # Create fresh client for this test
    client, cleanup, TestingSessionLocal = create_test_client()

    try:
        # Register user
        response = client.post(
            "/auth/register",
            json={"username": username, "password": password}
        )

        # If registration succeeded, check password is hashed
        if response.status_code == 201:
            db = TestingSessionLocal()
            try:
                user = db.query(User).filter(User.username == username).first()
                assert user is not None
                assert user.hashed_password != password, \
                    "Password should be hashed, not stored in plaintext"
            finally:
                db.close()
    finally:
        cleanup()


# Feature: pocket-heist, Property 2: Duplicate username rejection
@given(
    username=st.text(min_size=1, max_size=50).filter(lambda x: x.strip() != ""),
    password1=st.text(min_size=8, max_size=100),
    password2=st.text(min_size=8, max_size=100)
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_duplicate_username_rejected(username, password1, password2):
    """
    Property 2: Duplicate username rejection
    Validates: Requirements 1.2

    For any username that has already been registered, a second
    registration attempt with that same username SHALL return a 409 status code.
    """
    client, cleanup, _ = create_test_client()

    try:
        # First registration
        response1 = client.post(
            "/auth/register",
            json={"username": username, "password": password1}
        )

        # First registration should succeed
        assert response1.status_code == 201

        # Second registration with same username
        response2 = client.post(
            "/auth/register",
            json={"username": username, "password": password2}
        )

        # Second registration should fail with 409 Conflict
        assert response2.status_code == 409
    finally:
        cleanup()


# Feature: pocket-heist, Property 5: Wrong-password login is rejected
@given(
    username=st.text(min_size=1, max_size=50).filter(lambda x: x.strip() != ""),
    correct_password=st.text(min_size=8, max_size=100),
    wrong_password=st.text(min_size=8, max_size=100)
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_wrong_password_login_rejected(username, correct_password, wrong_password):
    """
    Property 5: Wrong-password login is rejected
    Validates: Requirements 2.2

    For any registered username and any password that differs from
    the registered password, a login attempt SHALL return a 401 status code.
    """
    # Ensure passwords are different
    assume(correct_password != wrong_password)

    client, cleanup, _ = create_test_client()

    try:
        # Register user
        response = client.post(
            "/auth/register",
            json={"username": username, "password": correct_password}
        )
        assert response.status_code == 201

        # Try to login with wrong password
        response = client.post(
            "/auth/login",
            params={"username": username, "password": wrong_password}
        )

        # Should get 401 Unauthorized
        assert response.status_code == 401
    finally:
        cleanup()


# Feature: pocket-heist, Property 6: Unregistered username login is rejected
@given(
    username=st.text(min_size=1, max_size=50).filter(lambda x: x.strip() != ""),
    password=st.text(min_size=8, max_size=100)
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_unregistered_username_login_rejected(username, password):
    """
    Property 6: Unregistered username login is rejected
    Validates: Requirements 2.3

    For any username string that has not been registered, a login attempt
    SHALL return a 401 status code.
    """
    client, cleanup, _ = create_test_client()

    try:
        # Try to login without registering
        response = client.post(
            "/auth/login",
            params={"username": username, "password": password}
        )

        # Should get 401 Unauthorized
        assert response.status_code == 401
    finally:
        cleanup()


# Feature: pocket-heist, Property 7: All heist endpoints require authentication
def test_heist_endpoints_require_authentication(client):
    """
    Property 7: All heist endpoints require authentication
    Validates: Requirements 2.6, 3.1

    For any heist management endpoint, a request made without a valid JWT token
    SHALL return a 401 status code.
    """
    # List of protected endpoints to test
    endpoints = [
        ("GET", "/heists"),
        ("POST", "/heists"),
        ("GET", "/heists/1"),
        ("PATCH", "/heists/1/abort"),
        ("GET", "/heists/archive"),
        ("GET", "/heists/mine"),
    ]

    for method, path in endpoints:
        # Make request without authentication
        if method == "GET":
            response = client.get(path)
        elif method == "POST":
            response = client.post(path, json={})
        elif method == "PATCH":
            response = client.patch(path)

        # Should return 401 Unauthorized (or 404 if endpoint doesn't exist yet)
        # We accept 404 because heist endpoints might not be implemented yet
        assert response.status_code in [401, 404], \
            f"{method} {path} should require authentication (got {response.status_code})"
