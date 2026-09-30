import logging

from app.db.database import SessionLocal
from app.db.repositories.whatsapp_repository import (
    get_message_by_id,
    update_message,
)
from app.services.grievance_service import (
    process_text_grievance,
    process_voice_grievance,
)
from app.services.whatsapp_service import download_media

logger = logging.getLogger(__name__)


def process_whatsapp_message(message_id: str):
    """Process one persisted Twilio WhatsApp message in the background."""
    db = SessionLocal()

    try:
        message = get_message_by_id(db, message_id)

        if not message:
            logger.warning("WhatsApp message not found: %s", message_id)
            return

        if message.processing_status == "PROCESSED":
            return

        if message.message_type == "audio":
            if not message.media_url:
                raise ValueError("Audio WhatsApp message has no media URL")

            update_message(
                db,
                message,
                {"processing_status": "PROCESSING", "error_message": None},
            )

            audio = download_media(message.media_url)
            result = process_voice_grievance(
                audio_bytes=audio,
                db=db,
                message=message,
            )

        elif message.message_type == "text":
            if not message.message_body:
                raise ValueError("Text WhatsApp message has an empty body")

            update_message(
                db,
                message,
                {"processing_status": "PROCESSING", "error_message": None},
            )

            result = process_text_grievance(
                text=message.message_body,
                db=db,
                message=message,
            )

        else:
            raise ValueError(
                f"Unsupported WhatsApp message type: {message.message_type}"
            )

        logger.info(
            "Civix grievance processed: message_id=%s grievance_id=%s hotspot_id=%s",
            message_id,
            getattr(result.get("grievance"), "id", None),
            getattr(result.get("hotspot"), "id", None),
        )

        update_message(
            db,
            message,
            {"processing_status": "PROCESSED", "error_message": None},
        )

    except Exception as exc:
        logger.exception("Failed to process WhatsApp message %s", message_id)
        db.rollback()

        message = get_message_by_id(db, message_id)
        if message:
            update_message(
                db,
                message,
                {
                    "processing_status": "FAILED",
                    "error_message": str(exc)[:4000],
                },
            )

    finally:
        db.close()
