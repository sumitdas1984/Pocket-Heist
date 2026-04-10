"""
Property-based tests for Pydantic schema validators
"""
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from pydantic import ValidationError
from datetime import datetime, timedelta

from backend.schemas import UserCreate, HeistCreate, HeistResponse, Difficulty, HeistStatus


# Feature: pocket-heist, Property 3: Short password rejection
@given(password=st.text(max_size=7))
@settings(max_examples=100)
def test_short_password_rejected(password):
    """
    Property 3: Short password rejection
    Validates: Requirements 1.3

    For any password string of length 0-7 characters,
    a registration attempt SHALL return a 422 status code.
    """
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(username="testuser", password=password)

    # Verify it's a validation error about minimum length
    errors = exc_info.value.errors()
    assert any('min_length' in str(error).lower() or 'at least 8' in str(error).lower()
               for error in errors)


# Feature: pocket-heist, Property 9: Invalid difficulty values are rejected
@given(difficulty_str=st.text().filter(
    lambda x: x not in ["Training", "Easy", "Medium", "Hard", "Legendary"]
))
@settings(max_examples=100)
def test_invalid_difficulty_rejected(difficulty_str):
    """
    Property 9: Invalid difficulty values are rejected
    Validates: Requirements 4.3

    For any string not in {Training, Easy, Medium, Hard, Legendary}
    supplied as the difficulty field, a heist creation request
    SHALL return a 422 status code.
    """
    future_deadline = datetime.utcnow() + timedelta(hours=1)

    # Try to create a heist with invalid difficulty value
    # This should raise a ValidationError when Pydantic tries to parse it
    with pytest.raises((ValidationError, ValueError)):
        # We need to pass the raw dict to trigger validation
        HeistCreate.model_validate({
            "title": "Test Heist",
            "target": "Test Target",
            "difficulty": difficulty_str,  # Invalid difficulty
            "assignee_username": "agent007",
            "deadline": future_deadline.isoformat(),
            "description": "Test description"
        })


# Feature: pocket-heist, Property 10: Past deadline is rejected
@given(past_datetime=st.datetimes(
    min_value=datetime(2000, 1, 1),
    max_value=datetime.utcnow() - timedelta(seconds=1)
))
@settings(max_examples=100)
def test_past_deadline_rejected(past_datetime):
    """
    Property 10: Past deadline is rejected
    Validates: Requirements 4.4

    For any datetime value that is in the past, supplying it as
    the deadline field in a heist creation request SHALL return
    a 422 status code.
    """
    with pytest.raises(ValidationError) as exc_info:
        HeistCreate(
            title="Test Heist",
            target="Test Target",
            difficulty=Difficulty.easy,
            assignee_username="agent007",
            deadline=past_datetime,
            description="Test description"
        )

    # Verify it's about the deadline being in the past
    errors = exc_info.value.errors()
    assert any('future' in str(error).lower() for error in errors)


# Feature: pocket-heist, Property 19: Heist serialization round-trip
@given(
    title=st.text(min_size=1, max_size=100),
    target=st.text(min_size=1, max_size=100),
    difficulty=st.sampled_from(list(Difficulty)),
    assignee=st.text(min_size=1, max_size=50),
    creator=st.text(min_size=1, max_size=50),
    description=st.one_of(st.none(), st.text(max_size=500)),
    status=st.sampled_from(list(HeistStatus)),
    heist_id=st.integers(min_value=1, max_value=1000000),
)
@settings(max_examples=100)
def test_heist_serialization_roundtrip(
    title, target, difficulty, assignee, creator, description, status, heist_id
):
    """
    Property 19: Heist serialization round-trip
    Validates: Requirements 11.4

    For any valid HeistResponse object, serializing it to JSON
    and deserializing it back SHALL produce an equivalent object
    with all fields preserved.
    """
    future_deadline = datetime.utcnow() + timedelta(hours=1)
    created_at = datetime.utcnow()

    # Create original HeistResponse
    original = HeistResponse(
        id=heist_id,
        title=title,
        target=target,
        difficulty=difficulty,
        assignee_username=assignee,
        creator_username=creator,
        deadline=future_deadline,
        description=description,
        status=status,
        created_at=created_at
    )

    # Serialize to JSON
    json_data = original.model_dump_json()

    # Deserialize back
    restored = HeistResponse.model_validate_json(json_data)

    # Verify all fields match
    assert restored.id == original.id
    assert restored.title == original.title
    assert restored.target == original.target
    assert restored.difficulty == original.difficulty
    assert restored.assignee_username == original.assignee_username
    assert restored.creator_username == original.creator_username
    assert restored.description == original.description
    assert restored.status == original.status

    # Datetime comparison (allowing for microsecond precision differences in JSON)
    assert abs((restored.deadline - original.deadline).total_seconds()) < 1
    assert abs((restored.created_at - original.created_at).total_seconds()) < 1
