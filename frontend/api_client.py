"""
API client for Pocket Heist backend
Wraps all backend API calls with requests library
"""
import requests
from typing import Optional, Dict, Any, List
import streamlit as st

# API base URL - update this if backend runs on different host/port
API_BASE_URL = "http://127.0.0.1:8000"


def get_headers() -> Dict[str, str]:
    """
    Get headers with JWT token from session state

    Returns:
        Dictionary with Authorization header if token exists
    """
    headers = {"Content-Type": "application/json"}

    if "access_token" in st.session_state:
        headers["Authorization"] = f"Bearer {st.session_state.access_token}"

    return headers


def register(username: str, password: str) -> Dict[str, Any]:
    """
    Register a new user

    Args:
        username: Username for registration
        password: Password (min 8 characters)

    Returns:
        User data dict or error dict

    Raises:
        requests.RequestException: On network errors
    """
    response = requests.post(
        f"{API_BASE_URL}/auth/register",
        json={"username": username, "password": password}
    )

    if response.status_code == 201:
        return response.json()
    else:
        return {"error": response.json().get("detail", "Registration failed")}


def login(username: str, password: str) -> Dict[str, Any]:
    """
    Login and get JWT token

    Args:
        username: Username
        password: Password

    Returns:
        Token data dict with 'access_token' or error dict

    Raises:
        requests.RequestException: On network errors
    """
    response = requests.post(
        f"{API_BASE_URL}/auth/login",
        params={"username": username, "password": password}
    )

    if response.status_code == 200:
        data = response.json()
        # Store token in session state
        st.session_state.access_token = data["access_token"]
        st.session_state.username = username
        return data
    else:
        return {"error": "Invalid credentials."}


def list_active_heists() -> List[Dict[str, Any]]:
    """
    List all active heists (War Room)

    Returns:
        List of active heist dicts

    Raises:
        requests.RequestException: On network errors
    """
    response = requests.get(
        f"{API_BASE_URL}/heists",
        headers=get_headers()
    )

    if response.status_code == 200:
        return response.json()
    else:
        return []


def list_archive_heists() -> List[Dict[str, Any]]:
    """
    List all archived heists (Expired/Aborted)

    Returns:
        List of archived heist dicts

    Raises:
        requests.RequestException: On network errors
    """
    response = requests.get(
        f"{API_BASE_URL}/heists/archive",
        headers=get_headers()
    )

    if response.status_code == 200:
        return response.json()
    else:
        return []


def list_my_heists() -> List[Dict[str, Any]]:
    """
    List heists created by current user

    Returns:
        List of user's heist dicts

    Raises:
        requests.RequestException: On network errors
    """
    response = requests.get(
        f"{API_BASE_URL}/heists/mine",
        headers=get_headers()
    )

    if response.status_code == 200:
        return response.json()
    else:
        return []


def create_heist(
    title: str,
    target: str,
    difficulty: str,
    assignee_username: str,
    deadline: str,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new heist

    Args:
        title: Mission name
        target: Target of the heist
        difficulty: Training | Easy | Medium | Hard | Legendary
        assignee_username: Username to assign heist to
        deadline: Deadline as ISO datetime string
        description: Optional mission details

    Returns:
        Created heist dict or error dict

    Raises:
        requests.RequestException: On network errors
    """
    heist_data = {
        "title": title,
        "target": target,
        "difficulty": difficulty,
        "assignee_username": assignee_username,
        "deadline": deadline,
        "description": description
    }

    response = requests.post(
        f"{API_BASE_URL}/heists",
        json=heist_data,
        headers=get_headers()
    )

    if response.status_code == 201:
        return response.json()
    else:
        error_detail = response.json().get("detail", "Blueprint incomplete. Fill all required fields.")
        return {"error": error_detail}


def abort_heist(heist_id: int) -> Dict[str, Any]:
    """
    Abort a heist (change status to Aborted)

    Args:
        heist_id: ID of heist to abort

    Returns:
        Updated heist dict or error dict

    Raises:
        requests.RequestException: On network errors
    """
    response = requests.patch(
        f"{API_BASE_URL}/heists/{heist_id}/abort",
        headers=get_headers()
    )

    if response.status_code == 200:
        return response.json()
    else:
        error_detail = response.json().get("detail", "Failed to abort heist")
        return {"error": error_detail}


def get_heist(heist_id: int) -> Optional[Dict[str, Any]]:
    """
    Get details of a specific heist

    Args:
        heist_id: ID of heist to retrieve

    Returns:
        Heist dict or None if not found

    Raises:
        requests.RequestException: On network errors
    """
    response = requests.get(
        f"{API_BASE_URL}/heists/{heist_id}",
        headers=get_headers()
    )

    if response.status_code == 200:
        return response.json()
    else:
        return None
