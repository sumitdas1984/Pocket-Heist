"""
Heist service layer for CRUD operations
"""
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.models import Heist, User
from backend.schemas import HeistCreate, HeistResponse
from backend.enums import HeistStatus


def create_heist(db: Session, heist_data: HeistCreate, creator: User) -> HeistResponse:
    """
    Create a new heist

    Args:
        db: Database session
        heist_data: Heist creation data
        creator: User creating the heist

    Returns:
        HeistResponse with created heist data
    """
    # Create new heist with Active status
    db_heist = Heist(
        title=heist_data.title,
        target=heist_data.target,
        difficulty=heist_data.difficulty,
        assignee_username=heist_data.assignee_username,
        creator_id=creator.id,
        deadline=heist_data.deadline,
        description=heist_data.description,
        status=HeistStatus.active  # Always start as Active
    )

    db.add(db_heist)
    db.commit()
    db.refresh(db_heist)

    # Build response with creator username
    return HeistResponse(
        id=db_heist.id,
        title=db_heist.title,
        target=db_heist.target,
        difficulty=db_heist.difficulty,
        assignee_username=db_heist.assignee_username,
        creator_username=creator.username,
        deadline=db_heist.deadline,
        description=db_heist.description,
        status=db_heist.status,
        created_at=db_heist.created_at
    )


def list_active_heists(db: Session) -> list[HeistResponse]:
    """
    List all active heists (deadline-aware)

    Returns only heists with:
    - status = Active
    - deadline > now()

    Args:
        db: Database session

    Returns:
        List of active HeistResponse objects
    """
    now = datetime.utcnow()

    # Query heists that are Active and deadline is in the future
    heists = db.query(Heist).filter(
        Heist.status == HeistStatus.active,
        Heist.deadline > now
    ).all()

    # Convert to response objects
    return [
        HeistResponse(
            id=heist.id,
            title=heist.title,
            target=heist.target,
            difficulty=heist.difficulty,
            assignee_username=heist.assignee_username,
            creator_username=heist.creator.username,
            deadline=heist.deadline,
            description=heist.description,
            status=heist.status,
            created_at=heist.created_at
        )
        for heist in heists
    ]


def list_archive_heists(db: Session) -> list[HeistResponse]:
    """
    List all archived heists (Expired or Aborted)

    Args:
        db: Database session

    Returns:
        List of archived HeistResponse objects
    """
    # Query heists that are Expired or Aborted
    heists = db.query(Heist).filter(
        Heist.status.in_([HeistStatus.expired, HeistStatus.aborted])
    ).all()

    # Convert to response objects
    return [
        HeistResponse(
            id=heist.id,
            title=heist.title,
            target=heist.target,
            difficulty=heist.difficulty,
            assignee_username=heist.assignee_username,
            creator_username=heist.creator.username,
            deadline=heist.deadline,
            description=heist.description,
            status=heist.status,
            created_at=heist.created_at
        )
        for heist in heists
    ]


def list_my_heists(db: Session, user: User) -> list[HeistResponse]:
    """
    List heists created by the requesting user

    Args:
        db: Database session
        user: Current user

    Returns:
        List of HeistResponse objects created by the user
    """
    # Query heists created by this user
    heists = db.query(Heist).filter(Heist.creator_id == user.id).all()

    # Convert to response objects
    return [
        HeistResponse(
            id=heist.id,
            title=heist.title,
            target=heist.target,
            difficulty=heist.difficulty,
            assignee_username=heist.assignee_username,
            creator_username=user.username,
            deadline=heist.deadline,
            description=heist.description,
            status=heist.status,
            created_at=heist.created_at
        )
        for heist in heists
    ]


def get_heist(db: Session, heist_id: int) -> HeistResponse:
    """
    Get a specific heist by ID

    Args:
        db: Database session
        heist_id: ID of the heist to retrieve

    Returns:
        HeistResponse object

    Raises:
        HTTPException 404: If heist not found
    """
    heist = db.query(Heist).filter(Heist.id == heist_id).first()

    if not heist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Heist with id {heist_id} not found"
        )

    return HeistResponse(
        id=heist.id,
        title=heist.title,
        target=heist.target,
        difficulty=heist.difficulty,
        assignee_username=heist.assignee_username,
        creator_username=heist.creator.username,
        deadline=heist.deadline,
        description=heist.description,
        status=heist.status,
        created_at=heist.created_at
    )


def abort_heist(db: Session, heist_id: int, requester: User) -> HeistResponse:
    """
    Abort a heist (change status to Aborted)

    Only the creator can abort a heist.
    Only Active heists can be aborted.

    Args:
        db: Database session
        heist_id: ID of the heist to abort
        requester: User requesting the abort

    Returns:
        HeistResponse with updated status

    Raises:
        HTTPException 404: If heist not found
        HTTPException 403: If requester is not the creator
        HTTPException 409: If heist is not Active
    """
    heist = db.query(Heist).filter(Heist.id == heist_id).first()

    # Check if heist exists
    if not heist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Heist with id {heist_id} not found"
        )

    # Check if requester is the creator
    if heist.creator_id != requester.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the creator can abort this heist"
        )

    # Check if heist is Active
    if heist.status != HeistStatus.active:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot abort heist with status {heist.status.value}"
        )

    # Update status to Aborted
    heist.status = HeistStatus.aborted
    db.commit()
    db.refresh(heist)

    return HeistResponse(
        id=heist.id,
        title=heist.title,
        target=heist.target,
        difficulty=heist.difficulty,
        assignee_username=heist.assignee_username,
        creator_username=heist.creator.username,
        deadline=heist.deadline,
        description=heist.description,
        status=heist.status,
        created_at=heist.created_at
    )
