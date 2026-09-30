from typing import Optional

from sqlalchemy.orm import Session

from app.models.grievance import Grievance


def create_grievance(
    db: Session,
    payload: dict,
):
    grievance = Grievance(**payload)

    db.add(grievance)
    db.commit()
    db.refresh(grievance)

    return grievance


def get_grievance(
    db: Session,
    grievance_id: int,
):
    return (
        db.query(Grievance)
        .filter(Grievance.id == grievance_id)
        .first()
    )


def get_grievance_by_whatsapp_message_id(
    db: Session,
    message_id: str,
):
    return (
        db.query(Grievance)
        .filter(
            Grievance.whatsapp_message_id
            == message_id
        )
        .first()
    )


def get_grievances(
    db: Session,
    *,
    status: Optional[str] = None,
    limit: int = 500,
):
    query = db.query(Grievance)

    if status:
        query = query.filter(
            Grievance.status == status
        )

    return (
        query
        .order_by(Grievance.id.desc())
        .limit(limit)
        .all()
    )


def update_grievance(
    db: Session,
    grievance,
    values: dict,
):
    for key, value in values.items():
        setattr(grievance, key, value)

    db.commit()
    db.refresh(grievance)

    return grievance