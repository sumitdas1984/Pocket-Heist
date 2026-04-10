"""
Smoke tests for API-first architecture requirements
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app
from backend.database import Base, get_db

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_smoke.db"
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


@pytest.fixture
def auth_token(client):
    """Register a user and return their auth token"""
    # Register user
    client.post(
        "/auth/register",
        json={"username": "testuser", "password": "password123"}
    )

    # Login and get token
    response = client.post(
        "/auth/login",
        params={"username": "testuser", "password": "password123"}
    )
    data = response.json()
    return data["access_token"]


def test_docs_endpoint_accessible(client):
    """
    Test /docs endpoint is accessible
    Validates: Requirement 12.1

    The OpenAPI documentation SHALL be accessible at /docs
    for API exploration and integration testing.
    """
    response = client.get("/docs")

    # Should return 200 OK
    assert response.status_code == 200

    # Should return HTML
    assert "text/html" in response.headers.get("content-type", "")

    # Should contain Swagger UI
    assert "swagger" in response.text.lower() or "openapi" in response.text.lower()


def test_cors_headers_present_on_heist_endpoints(client, auth_token):
    """
    Test CORS headers are present on heist endpoints
    Validates: Requirement 12.2

    All API endpoints SHALL include proper CORS headers to allow
    access from frontend applications running on different origins.
    """
    # Test CORS preflight (OPTIONS) request
    response = client.options(
        "/heists",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization"
        }
    )

    # Should allow the origin
    assert "access-control-allow-origin" in response.headers
    allowed_origin = response.headers["access-control-allow-origin"]
    assert allowed_origin in ["http://localhost:3000", "*"]

    # Should allow methods
    assert "access-control-allow-methods" in response.headers

    # Should allow headers
    assert "access-control-allow-headers" in response.headers


def test_cors_headers_on_actual_request(client, auth_token):
    """Test CORS headers are present on actual API requests"""
    response = client.get(
        "/heists",
        headers={
            "Origin": "http://localhost:8501",  # Streamlit default port
            "Authorization": f"Bearer {auth_token}"
        }
    )

    # Should have CORS header in response
    assert "access-control-allow-origin" in response.headers


def test_all_list_endpoints_return_json(client, auth_token):
    """
    Test all list endpoints return JSON content-type
    Validates: Requirement 12.3

    All API endpoints SHALL return responses with
    Content-Type: application/json for consistent parsing.
    """
    headers = {"Authorization": f"Bearer {auth_token}"}

    # List of all list endpoints
    list_endpoints = [
        "/heists",
        "/heists/archive",
        "/heists/mine"
    ]

    for endpoint in list_endpoints:
        response = client.get(endpoint, headers=headers)

        # Should return successful response
        assert response.status_code == 200, f"{endpoint} should return 200"

        # Should have JSON content-type
        content_type = response.headers.get("content-type", "")
        assert "application/json" in content_type, \
            f"{endpoint} should return application/json, got {content_type}"

        # Should return valid JSON (list)
        data = response.json()
        assert isinstance(data, list), f"{endpoint} should return a JSON array"


def test_create_endpoint_returns_json(client, auth_token):
    """Test POST /heists returns JSON"""
    from datetime import datetime, timedelta

    future_deadline = datetime.utcnow() + timedelta(hours=3)

    heist_data = {
        "title": "Test Mission",
        "target": "Test Target",
        "difficulty": "Medium",
        "assignee_username": "agent",
        "deadline": future_deadline.isoformat()
    }

    response = client.post(
        "/heists",
        json=heist_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    # Should return 201 Created
    assert response.status_code == 201

    # Should have JSON content-type
    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type

    # Should return valid JSON object
    data = response.json()
    assert isinstance(data, dict)
    assert "id" in data


def test_auth_endpoints_return_json(client):
    """Test authentication endpoints return JSON"""
    # Register endpoint
    register_response = client.post(
        "/auth/register",
        json={"username": "jsonuser", "password": "password123"}
    )

    assert register_response.status_code == 201
    assert "application/json" in register_response.headers.get("content-type", "")
    assert isinstance(register_response.json(), dict)

    # Login endpoint
    login_response = client.post(
        "/auth/login",
        params={"username": "jsonuser", "password": "password123"}
    )

    assert login_response.status_code == 200
    assert "application/json" in login_response.headers.get("content-type", "")
    assert isinstance(login_response.json(), dict)
    assert "access_token" in login_response.json()


def test_error_responses_return_json(client, auth_token):
    """Test that error responses also return JSON"""
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Test 404 error
    response_404 = client.get("/heists/999999", headers=headers)
    assert response_404.status_code == 404
    assert "application/json" in response_404.headers.get("content-type", "")
    assert "detail" in response_404.json()

    # Test 401 error (no token)
    response_401 = client.get("/heists")
    assert response_401.status_code == 401
    assert "application/json" in response_401.headers.get("content-type", "")

    # Test 422 validation error
    invalid_heist = {
        "title": "Test",
        "target": "Target",
        "difficulty": "Invalid",  # Invalid difficulty
        "assignee_username": "agent",
        "deadline": "2026-04-15T12:00:00"
    }

    response_422 = client.post(
        "/heists",
        json=invalid_heist,
        headers=headers
    )
    assert response_422.status_code == 422
    assert "application/json" in response_422.headers.get("content-type", "")


def test_api_is_stateless(client):
    """
    Test that API is stateless (no server-side sessions)
    Validates: API-first architecture principle

    The API SHALL be stateless, relying on JWT tokens for authentication
    rather than server-side sessions.
    """
    # Register and login to get token
    client.post("/auth/register", json={"username": "stateless", "password": "password123"})
    login_response = client.post("/auth/login", params={"username": "stateless", "password": "password123"})
    token = login_response.json()["access_token"]

    # Make request with token
    response1 = client.get("/heists", headers={"Authorization": f"Bearer {token}"})
    assert response1.status_code == 200

    # Make another request with same token (should work - stateless)
    response2 = client.get("/heists", headers={"Authorization": f"Bearer {token}"})
    assert response2.status_code == 200

    # Token should work independently of previous requests
    response3 = client.get("/heists/mine", headers={"Authorization": f"Bearer {token}"})
    assert response3.status_code == 200
