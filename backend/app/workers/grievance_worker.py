import logging

from app.db.database import SessionLocal
from app.db.repositories.whatsapp_repository import (
    get_message_by_id,
    update_message,
)
from app.services.grievance_service import process_voice_grievance
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

        if message.message_type != "audio" or not message.media_url:
            update_message(
                db,
                message,
                {"processing_status": "RECEIVED"},
            )
            return

        update_message(
            db,
            message,
            {
                "processing_status": "PROCESSING",
                "error_message": None,
            },
        )

        audio = download_media(message.media_url)

        result = process_voice_grievance(
            audio_bytes=audio,
        )

        logger.info(
            "Civix grievance processed: message_id=%s result=%s",
            message_id,
            result,
        )

        update_message(
            db,
            message,
            {"processing_status": "PROCESSED"},
        )

    except Exception as exc:
        logger.exception(
            "Failed to process WhatsApp message %s",
            message_id,
        )

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
