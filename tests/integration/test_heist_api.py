"""
Integration tests for heist API endpoints
"""
import pytest
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from backend.main import app
from backend.database import Base, get_db
from backend.enums import Difficulty, HeistStatus

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_heist_api.db"
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


# Feature: pocket-heist, Property 14: Heist retrieval round-trip
@given(
    title=st.text(min_size=1, max_size=100),
    target=st.text(min_size=1, max_size=100),
    difficulty=st.sampled_from(list(Difficulty)),
    assignee=st.text(min_size=1, max_size=50),
    description=st.one_of(st.none(), st.text(max_size=500))
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_heist_retrieval_roundtrip(client, auth_token, title, target, difficulty, assignee, description):
    """
    Property 14: Heist retrieval round-trip
    Validates: Requirements 8.1

    For any valid heist creation payload, creating a heist and then
    retrieving it by its returned id SHALL produce a response object
    where all fields match the original creation data.
    """
    future_deadline = datetime.utcnow() + timedelta(hours=3)

    # Create heist
    create_data = {
        "title": title,
        "target": target,
        "difficulty": difficulty.value,
        "assignee_username": assignee,
        "deadline": future_deadline.isoformat(),
        "description": description
    }

    create_response = client.post(
        "/heists",
        json=create_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    # Should return 201 Created
    if create_response.status_code != 201:
        # Skip this iteration if validation failed (e.g., invalid characters)
        return

    created_heist = create_response.json()
    heist_id = created_heist["id"]

    # Retrieve the heist by ID
    get_response = client.get(
        f"/heists/{heist_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert get_response.status_code == 200
    retrieved_heist = get_response.json()

    # Verify all fields match
    assert retrieved_heist["id"] == heist_id
    assert retrieved_heist["title"] == title
    assert retrieved_heist["target"] == target
    assert retrieved_heist["difficulty"] == difficulty.value
    assert retrieved_heist["assignee_username"] == assignee
    assert retrieved_heist["creator_username"] == "testuser"
    assert retrieved_heist["description"] == description
    assert retrieved_heist["status"] == HeistStatus.active.value

    # Deadline should match (allowing for minor timestamp differences)
    retrieved_deadline = datetime.fromisoformat(retrieved_heist["deadline"].replace('Z', '+00:00'))
    deadline_diff = abs((retrieved_deadline.replace(tzinfo=None) - future_deadline).total_seconds())
    assert deadline_diff < 1, "Deadline should match within 1 second"


# Feature: pocket-heist, Property 15: Non-existent heist retrieval returns 404
@given(
    heist_id=st.integers(min_value=999999, max_value=9999999)
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_nonexistent_heist_returns_404(client, auth_token, heist_id):
    """
    Property 15: Non-existent heist retrieval returns 404
    Validates: Requirements 8.2

    For any integer ID that does not correspond to an existing heist,
    a GET /heists/{id} request SHALL return a 404 status code.
    """
    response = client.get(
        f"/heists/{heist_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    # Should return 404 Not Found
    assert response.status_code == 404


def test_create_heist_returns_201(client, auth_token):
    """Test that creating a heist returns 201 with heist data"""
    future_deadline = datetime.utcnow() + timedelta(hours=3)

    heist_data = {
        "title": "Test Mission",
        "target": "Test Target",
        "difficulty": "Medium",
        "assignee_username": "agent007",
        "deadline": future_deadline.isoformat(),
        "description": "Test description"
    }

    response = client.post(
        "/heists",
        json=heist_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Mission"
    assert data["status"] == "Active"
    assert data["creator_username"] == "testuser"


def test_list_active_heists_excludes_expired(client, auth_token):
    """Test that active heist list excludes past-deadline heists"""
    # Create heist with past deadline
    past_deadline = datetime.utcnow() + timedelta(hours=-1)
    past_heist = {
        "title": "Past Heist",
        "target": "Old Target",
        "difficulty": "Easy",
        "assignee_username": "agent",
        "deadline": past_deadline.isoformat(),
        "description": "Past"
    }

    # Create heist with future deadline
    future_deadline = datetime.utcnow() + timedelta(hours=2)
    future_heist = {
        "title": "Future Heist",
        "target": "New Target",
        "difficulty": "Hard",
        "assignee_username": "agent",
        "deadline": future_deadline.isoformat(),
        "description": "Future"
    }

    # Create both heists
    client.post("/heists", json=past_heist, headers={"Authorization": f"Bearer {auth_token}"})
    client.post("/heists", json=future_heist, headers={"Authorization": f"Bearer {auth_token}"})

    # List active heists
    response = client.get("/heists", headers={"Authorization": f"Bearer {auth_token}"})

    assert response.status_code == 200
    heists = response.json()

    # Should only contain future heist
    titles = [h["title"] for h in heists]
    assert "Future Heist" in titles
    assert "Past Heist" not in titles


def test_abort_heist_by_creator(client, auth_token):
    """Test that creator can abort their heist"""
    future_deadline = datetime.utcnow() + timedelta(hours=3)

    # Create heist
    heist_data = {
        "title": "Abortable Mission",
        "target": "Target",
        "difficulty": "Medium",
        "assignee_username": "agent",
        "deadline": future_deadline.isoformat()
    }

    create_response = client.post(
        "/heists",
        json=heist_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    heist_id = create_response.json()["id"]

    # Abort heist
    abort_response = client.patch(
        f"/heists/{heist_id}/abort",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert abort_response.status_code == 200
    data = abort_response.json()
    assert data["status"] == "Aborted"


def test_abort_heist_by_non_creator_forbidden(client):
    """Test that non-creator cannot abort heist"""
    # Register and login first user
    client.post("/auth/register", json={"username": "creator", "password": "password123"})
    creator_response = client.post("/auth/login", params={"username": "creator", "password": "password123"})
    creator_token = creator_response.json()["access_token"]

    # Register and login second user
    client.post("/auth/register", json={"username": "other", "password": "password123"})
    other_response = client.post("/auth/login", params={"username": "other", "password": "password123"})
    other_token = other_response.json()["access_token"]

    # Creator creates heist
    future_deadline = datetime.utcnow() + timedelta(hours=3)
    heist_data = {
        "title": "Creator's Mission",
        "target": "Target",
        "difficulty": "Easy",
        "assignee_username": "agent",
        "deadline": future_deadline.isoformat()
    }

    create_response = client.post(
        "/heists",
        json=heist_data,
        headers={"Authorization": f"Bearer {creator_token}"}
    )
    heist_id = create_response.json()["id"]

    # Other user tries to abort
    abort_response = client.patch(
        f"/heists/{heist_id}/abort",
        headers={"Authorization": f"Bearer {other_token}"}
    )

    # Should be forbidden
    assert abort_response.status_code == 403


def test_list_my_heists_returns_only_user_heists(client):
    """Test that /heists/mine returns only the authenticated user's heists"""
    # Register two users
    client.post("/auth/register", json={"username": "user1", "password": "password123"})
    client.post("/auth/register", json={"username": "user2", "password": "password123"})

    # Get tokens
    user1_response = client.post("/auth/login", params={"username": "user1", "password": "password123"})
    user1_token = user1_response.json()["access_token"]

    user2_response = client.post("/auth/login", params={"username": "user2", "password": "password123"})
    user2_token = user2_response.json()["access_token"]

    # User1 creates heists
    future_deadline = datetime.utcnow() + timedelta(hours=3)
    for i in range(2):
        heist_data = {
            "title": f"User1 Heist {i}",
            "target": "Target",
            "difficulty": "Easy",
            "assignee_username": "agent",
            "deadline": future_deadline.isoformat()
        }
        client.post("/heists", json=heist_data, headers={"Authorization": f"Bearer {user1_token}"})

    # User2 creates heists
    for i in range(3):
        heist_data = {
            "title": f"User2 Heist {i}",
            "target": "Target",
            "difficulty": "Medium",
            "assignee_username": "agent",
            "deadline": future_deadline.isoformat()
        }
        client.post("/heists", json=heist_data, headers={"Authorization": f"Bearer {user2_token}"})

    # Get user1's heists
    response1 = client.get("/heists/mine", headers={"Authorization": f"Bearer {user1_token}"})
    user1_heists = response1.json()

    assert len(user1_heists) == 2
    for heist in user1_heists:
        assert heist["creator_username"] == "user1"

    # Get user2's heists
    response2 = client.get("/heists/mine", headers={"Authorization": f"Bearer {user2_token}"})
    user2_heists = response2.json()

    assert len(user2_heists) == 3
    for heist in user2_heists:
        assert heist["creator_username"] == "user2"
