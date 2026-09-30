import logging
import os
import time

from app.db.database import SessionLocal
from app.db.repositories.whatsapp_repository import get_messages
from app.workers.grievance_worker import process_whatsapp_message

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("civix.worker")

POLL_SECONDS = int(os.getenv("WORKER_POLL_SECONDS", "2"))


def claim_next_message():
    db = SessionLocal()
    try:
        messages = get_messages(db, processing_status="RECEIVED", limit=20)
        for message in messages:
            if message.message_type == "audio" and message.media_url:
                return message.message_id
            if message.message_type == "text" and message.message_body:
                return message.message_id
    finally:
        db.close()
    return None


def main():
    logger.info("Civix grievance worker started")
    while True:
        try:
            message_id = claim_next_message()
            if message_id:
                logger.info("Processing WhatsApp message %s", message_id)
                process_whatsapp_message(message_id)
            else:
                time.sleep(POLL_SECONDS)
        except Exception:
            logger.exception("Worker loop failed")
            time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
