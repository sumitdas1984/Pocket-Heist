"""
Property-based tests for JWT authentication
"""
from hypothesis import given, settings
from hypothesis import strategies as st
from datetime import datetime

from backend.auth import create_access_token, decode_access_token, verify_token


# Feature: pocket-heist, Property 4: Login round-trip produces a valid JWT
@given(
    username=st.text(min_size=1, max_size=50),
    user_id=st.integers(min_value=1, max_value=1000000)
)
@settings(max_examples=100)
def test_jwt_roundtrip_valid_expiry(username, user_id):
    """
    Property 4: Login round-trip produces a valid JWT
    Validates: Requirements 2.1, 2.4

    For any successfully registered (username, password) pair,
    a login request with those credentials SHALL return a 200 status code
    and a JWT token whose decoded exp - iat is at most 86400 seconds (24 hours).
    """
    # Create token with user data
    token_data = {
        "sub": username,
        "user_id": user_id
    }
    token = create_access_token(data=token_data)

    # Verify token is a non-empty string
    assert isinstance(token, str)
    assert len(token) > 0

    # Decode token
    payload = decode_access_token(token)

    # Verify payload contains expected fields
    assert payload["sub"] == username
    assert payload["user_id"] == user_id
    assert "exp" in payload
    assert "iat" in payload

    # Verify expiration is at most 24 hours (86400 seconds) from issued time
    exp = payload["exp"]
    iat = payload["iat"]
    token_lifetime = exp - iat

    assert token_lifetime <= 86400, f"Token lifetime {token_lifetime}s exceeds 24 hours (86400s)"
    assert token_lifetime > 0, "Token expiration must be after issued time"


@given(
    username=st.text(min_size=1, max_size=50),
    user_id=st.integers(min_value=1, max_value=1000000)
)
@settings(max_examples=100)
def test_token_verification_succeeds(username, user_id):
    """Test that valid tokens pass verification"""
    token = create_access_token(data={"sub": username, "user_id": user_id})

    payload = verify_token(token)

    assert payload is not None
    assert payload["sub"] == username
    assert payload["user_id"] == user_id


def test_invalid_token_verification_fails():
    """Test that invalid tokens fail verification"""
    invalid_tokens = [
        "not-a-valid-token",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.signature",
        "",
        "Bearer token",
    ]

    for invalid_token in invalid_tokens:
        payload = verify_token(invalid_token)
        assert payload is None, f"Invalid token '{invalid_token}' should not verify"
