"""
Property-based tests for heist service layer
"""
import pytest
from hypothesis import given, settings, assume, HealthCheck
from hypothesis import strategies as st
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base
from backend.models import User, Heist
from backend.schemas import HeistCreate
from backend.enums import Difficulty, HeistStatus
from backend.heist_service import (
    create_heist,
    list_active_heists,
    list_archive_heists,
    list_my_heists,
    abort_heist
)

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_heist_service.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    """Setup and teardown database for each test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    """Get database session"""
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture
def test_user(db):
    """Create a test user"""
    user = User(username="testuser", hashed_password="hashedpass123")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Feature: pocket-heist, Property 8: Heist creation sets creator and Active status
@given(
    title=st.text(min_size=1, max_size=100),
    target=st.text(min_size=1, max_size=100),
    difficulty=st.sampled_from(list(Difficulty)),
    assignee=st.text(min_size=1, max_size=50),
    description=st.one_of(st.none(), st.text(max_size=500))
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_heist_creation_sets_creator_and_active_status(
    db, test_user, title, target, difficulty, assignee, description
):
    """
    Property 8: Heist creation sets creator and Active status
    Validates: Requirements 4.5, 4.6

    For any authenticated user and any valid heist creation payload,
    the created heist SHALL have creator_username equal to the authenticated
    user's username and status equal to Active.
    """
    future_deadline = datetime.utcnow() + timedelta(hours=3)

    # Create heist data
    heist_data = HeistCreate(
        title=title,
        target=target,
        difficulty=difficulty,
        assignee_username=assignee,
        deadline=future_deadline,
        description=description
    )

    # Create heist
    result = create_heist(db, heist_data, test_user)

    # Verify creator username matches
    assert result.creator_username == test_user.username

    # Verify status is Active
    assert result.status == HeistStatus.active


# Feature: pocket-heist, Property 11: Active heist list excludes past-deadline heists
def test_active_heist_list_excludes_past_deadline(db, test_user):
    """
    Property 11: Active heist list excludes past-deadline heists
    Validates: Requirements 5.1, 10.1, 10.2

    For any set of heists in the database, a request to list active heists
    SHALL return only heists whose deadline is strictly in the future and
    whose status is Active; no heist with a past deadline SHALL appear.
    """
    # Create a heist with past deadline but Active status
    past_deadline = datetime.utcnow() + timedelta(hours=-2)

    heist = Heist(
        title="Past Heist",
        target="Old Target",
        difficulty=Difficulty.easy,
        assignee_username="agent",
        creator_id=test_user.id,
        deadline=past_deadline,
        status=HeistStatus.active,
        description="Past deadline"
    )
    db.add(heist)

    # Create a heist with future deadline and Active status
    future_deadline = datetime.utcnow() + timedelta(hours=2)
    future_heist = Heist(
        title="Future Heist",
        target="Future Target",
        difficulty=Difficulty.medium,
        assignee_username="agent",
        creator_id=test_user.id,
        deadline=future_deadline,
        status=HeistStatus.active,
        description="Future deadline"
    )
    db.add(future_heist)
    db.commit()

    # List active heists
    active_heists = list_active_heists(db)

    # Past deadline heist should not be in the list
    past_heist_ids = [h.id for h in active_heists if h.deadline <= datetime.utcnow()]
    assert len(past_heist_ids) == 0, "No heists with past deadlines should appear"

    # Future heist should be in the list
    future_heist_ids = [h.id for h in active_heists if h.title == "Future Heist"]
    assert len(future_heist_ids) == 1, "Future heist should appear in active list"


# Feature: pocket-heist, Property 12: Archive list contains only Expired or Aborted heists
def test_archive_list_contains_only_expired_or_aborted(db, test_user):
    """
    Property 12: Archive list contains only Expired or Aborted heists
    Validates: Requirements 7.1

    For any set of heists in the database, a request to list the archive
    SHALL return only heists with status equal to Expired or Aborted;
    no Active heist SHALL appear.
    """
    num_active = 2
    num_expired = 3
    num_aborted = 2

    future_deadline = datetime.utcnow() + timedelta(hours=1)

    # Create Active heists
    for i in range(num_active):
        heist = Heist(
            title=f"Active {i}",
            target=f"Target {i}",
            difficulty=Difficulty.easy,
            assignee_username="agent",
            creator_id=test_user.id,
            deadline=future_deadline,
            status=HeistStatus.active
        )
        db.add(heist)

    # Create Expired heists
    for i in range(num_expired):
        heist = Heist(
            title=f"Expired {i}",
            target=f"Target {i}",
            difficulty=Difficulty.medium,
            assignee_username="agent",
            creator_id=test_user.id,
            deadline=future_deadline,
            status=HeistStatus.expired
        )
        db.add(heist)

    # Create Aborted heists
    for i in range(num_aborted):
        heist = Heist(
            title=f"Aborted {i}",
            target=f"Target {i}",
            difficulty=Difficulty.hard,
            assignee_username="agent",
            creator_id=test_user.id,
            deadline=future_deadline,
            status=HeistStatus.aborted
        )
        db.add(heist)

    db.commit()

    # List archive heists
    archive_heists = list_archive_heists(db)

    # Verify no Active heists in archive
    active_in_archive = [h for h in archive_heists if h.status == HeistStatus.active]
    assert len(active_in_archive) == 0, "No Active heists should appear in archive"

    # Verify only Expired or Aborted
    for heist in archive_heists:
        assert heist.status in [HeistStatus.expired, HeistStatus.aborted]

    # Verify count matches
    assert len(archive_heists) == num_expired + num_aborted


# Feature: pocket-heist, Property 13: My-heists list contains only the requesting user's heists
def test_my_heists_list_contains_only_user_heists(db):
    """
    Property 13: My-heists list contains only the requesting user's heists
    Validates: Requirements 6.1

    For any authenticated user, a request to list their own heists
    SHALL return only heists where creator_username equals that user's username;
    heists created by other users SHALL NOT appear.
    """
    # Create two users
    user1 = User(username="user1", hashed_password="hash1")
    user2 = User(username="user2", hashed_password="hash2")
    db.add(user1)
    db.add(user2)
    db.commit()
    db.refresh(user1)
    db.refresh(user2)

    future_deadline = datetime.utcnow() + timedelta(hours=1)

    # Create heists for user1
    for i in range(3):
        heist = Heist(
            title=f"User1 Heist {i}",
            target=f"Target {i}",
            difficulty=Difficulty.easy,
            assignee_username="agent",
            creator_id=user1.id,
            deadline=future_deadline,
            status=HeistStatus.active
        )
        db.add(heist)

    # Create heists for user2
    for i in range(2):
        heist = Heist(
            title=f"User2 Heist {i}",
            target=f"Target {i}",
            difficulty=Difficulty.medium,
            assignee_username="agent",
            creator_id=user2.id,
            deadline=future_deadline,
            status=HeistStatus.active
        )
        db.add(heist)

    db.commit()

    # List heists for user1
    user1_heists = list_my_heists(db, user1)

    # Verify only user1's heists
    assert len(user1_heists) == 3
    for heist in user1_heists:
        assert heist.creator_username == user1.username

    # List heists for user2
    user2_heists = list_my_heists(db, user2)

    # Verify only user2's heists
    assert len(user2_heists) == 2
    for heist in user2_heists:
        assert heist.creator_username == user2.username


# Feature: pocket-heist, Property 16: Abort by non-creator is forbidden
def test_abort_by_non_creator_forbidden(db):
    """
    Property 16: Abort by non-creator is forbidden
    Validates: Requirements 9.2

    For any heist and any authenticated user who is not the creator of that heist,
    an abort request SHALL return a 403 status code.
    """
    # Create two users
    creator = User(username="creator", hashed_password="hash1")
    other_user = User(username="other", hashed_password="hash2")
    db.add(creator)
    db.add(other_user)
    db.commit()
    db.refresh(creator)
    db.refresh(other_user)

    # Create heist by creator
    future_deadline = datetime.utcnow() + timedelta(hours=1)
    heist = Heist(
        title="Test Heist",
        target="Test Target",
        difficulty=Difficulty.easy,
        assignee_username="agent",
        creator_id=creator.id,
        deadline=future_deadline,
        status=HeistStatus.active
    )
    db.add(heist)
    db.commit()
    db.refresh(heist)

    # Try to abort by non-creator
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc_info:
        abort_heist(db, heist.id, other_user)

    # Should be 403 Forbidden
    assert exc_info.value.status_code == 403


# Feature: pocket-heist, Property 17: Abort transitions Active heist to Aborted
@given(
    title=st.text(min_size=1, max_size=100),
    target=st.text(min_size=1, max_size=100)
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_abort_transitions_active_to_aborted(db, test_user, title, target):
    """
    Property 17: Abort transitions Active heist to Aborted
    Validates: Requirements 9.1

    For any Active heist, an abort request by its creator SHALL return
    a 200 status code and the heist's status SHALL be Aborted when
    subsequently retrieved.
    """
    # Create Active heist
    future_deadline = datetime.utcnow() + timedelta(hours=1)
    heist = Heist(
        title=title,
        target=target,
        difficulty=Difficulty.medium,
        assignee_username="agent",
        creator_id=test_user.id,
        deadline=future_deadline,
        status=HeistStatus.active
    )
    db.add(heist)
    db.commit()
    db.refresh(heist)

    # Abort heist
    result = abort_heist(db, heist.id, test_user)

    # Verify status is now Aborted
    assert result.status == HeistStatus.aborted

    # Verify in database
    db.refresh(heist)
    assert heist.status == HeistStatus.aborted


# Feature: pocket-heist, Property 18: Aborting a non-Active heist returns 409
@given(
    status=st.sampled_from([HeistStatus.expired, HeistStatus.aborted])
)
@settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_aborting_non_active_heist_returns_409(db, test_user, status):
    """
    Property 18: Aborting a non-Active heist returns 409
    Validates: Requirements 9.3

    For any heist with status Expired or Aborted, an abort request
    SHALL return a 409 status code.
    """
    # Create heist with non-Active status
    future_deadline = datetime.utcnow() + timedelta(hours=1)
    heist = Heist(
        title="Non-Active Heist",
        target="Test Target",
        difficulty=Difficulty.hard,
        assignee_username="agent",
        creator_id=test_user.id,
        deadline=future_deadline,
        status=status
    )
    db.add(heist)
    db.commit()
    db.refresh(heist)

    # Try to abort non-Active heist
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc_info:
        abort_heist(db, heist.id, test_user)

    # Should be 409 Conflict
    assert exc_info.value.status_code == 409
