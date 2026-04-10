"""
Heist API endpoints
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models import User
from backend.schemas import HeistCreate, HeistResponse
from backend.heist_service import (
    create_heist,
    list_active_heists,
    list_archive_heists,
    list_my_heists,
    get_heist,
    abort_heist
)

router = APIRouter(prefix="/heists", tags=["heists"])


@router.get("", response_model=list[HeistResponse])
def get_active_heists(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all active heists (War Room)

    Returns heists with:
    - status = Active
    - deadline > now()

    Requires authentication.
    """
    return list_active_heists(db)


@router.post("", response_model=HeistResponse, status_code=status.HTTP_201_CREATED)
def create_new_heist(
    heist_data: HeistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new heist

    - **title**: Mission name
    - **target**: Target of the heist
    - **difficulty**: Training | Easy | Medium | Hard | Legendary
    - **assignee_username**: Username to assign this heist to
    - **deadline**: Deadline (must be in the future)
    - **description**: Optional mission details

    Requires authentication. Creator is set to the authenticated user.
    """
    return create_heist(db, heist_data, current_user)


@router.get("/archive", response_model=list[HeistResponse])
def get_archive_heists(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List archived heists (Mission Archive)

    Returns heists with status = Expired or Aborted.

    Requires authentication.
    """
    return list_archive_heists(db)


@router.get("/mine", response_model=list[HeistResponse])
def get_my_heists(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List heists created by the current user

    Returns only heists where creator_username equals the authenticated user's username.

    Requires authentication.
    """
    return list_my_heists(db, current_user)


@router.get("/{heist_id}", response_model=HeistResponse)
def get_heist_details(
    heist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get details of a specific heist

    Returns heist data by ID.

    Requires authentication.
    """
    return get_heist(db, heist_id)


@router.patch("/{heist_id}/abort", response_model=HeistResponse)
def abort_heist_by_id(
    heist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Abort a heist

    Changes heist status from Active to Aborted.

    - Only the creator can abort their heist (403 if not creator)
    - Only Active heists can be aborted (409 if not Active)

    Requires authentication.
    """
    return abort_heist(db, heist_id, current_user)
