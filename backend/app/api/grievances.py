from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.grievance import Grievance


router = APIRouter(
    prefix="/grievances",
    tags=["Grievances"]
)


@router.get("")
def get_grievances(
    db: Session = Depends(get_db)
):

    return (
        db.query(Grievance)
        .order_by(
            Grievance.id.desc()
        )
        .all()
    )


@router.get("/{grievance_id}")
def get_grievance(
    grievance_id: int,
    db: Session = Depends(get_db)
):

    return (
        db.query(Grievance)
        .filter(
            Grievance.id == grievance_id
        )
        .first()
    )