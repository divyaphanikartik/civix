from typing import Optional

from sqlalchemy.orm import Session

from app.models.whatsapp import WhatsAppMessage


def create_message(db: Session, payload: dict):
    message = WhatsAppMessage(**payload)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_message_by_id(db: Session, message_id: str):
    return (
        db.query(WhatsAppMessage)
        .filter(WhatsAppMessage.message_id == message_id)
        .first()
    )


def update_message(db: Session, message, values: dict):
    for key, value in values.items():
        setattr(message, key, value)
    db.commit()
    db.refresh(message)
    return message


def get_messages(
    db: Session,
    *,
    processing_status: Optional[str] = None,
    limit: int = 500,
):
    query = db.query(WhatsAppMessage)

    if processing_status:
        query = query.filter(
            WhatsAppMessage.processing_status == processing_status
        )

    return (
        query
        .order_by(WhatsAppMessage.id.desc())
        .limit(limit)
        .all()
    )
