import logging

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from fastapi.responses import Response
from sqlalchemy.exc import IntegrityError
from twilio.twiml.messaging_response import MessagingResponse

from app.config import settings
from app.db.database import SessionLocal
from app.db.repositories.whatsapp_repository import (
    create_message,
    get_message_by_id,
)
from app.services.whatsapp_service import validate_webhook_signature
from app.workers.grievance_worker import process_whatsapp_message

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/webhooks",
    tags=["WhatsApp"],
)


def _twiml_response(body: str | None = None) -> Response:
    response = MessagingResponse()

    if body:
        response.message(body)

    return Response(
        content=str(response),
        media_type="application/xml",
    )


@router.post("/whatsapp")
async def whatsapp_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
):
    """Receive inbound WhatsApp messages from Twilio."""
    form = await request.form()
    params = dict(form)

    signature = request.headers.get("X-Twilio-Signature")

    if not validate_webhook_signature(
        str(request.url),
        params,
        signature,
    ):
        raise HTTPException(
            status_code=403,
            detail="Invalid Twilio webhook signature",
        )

    message_id = form.get("MessageSid")
    sender = form.get("From")
    recipient = form.get("To")
    message_type = "audio" if int(form.get("NumMedia", "0")) > 0 else "text"

    media_url = None
    media_content_type = None

    if message_type == "audio":
        for index in range(int(form.get("NumMedia", "0"))):
            content_type = form.get(f"MediaContentType{index}")
            candidate_url = form.get(f"MediaUrl{index}")

            if content_type and content_type.startswith("audio/"):
                media_url = candidate_url
                media_content_type = content_type
                break

        if not media_url:
            message_type = "media"

    if not message_id or not sender:
        raise HTTPException(
            status_code=400,
            detail="Missing Twilio MessageSid or From",
        )

    db = SessionLocal()

    try:
        existing = get_message_by_id(db, message_id)

        if not existing:
            payload = {
                "message_id": message_id,
                "sender_phone": sender,
                "recipient_phone": recipient,
                "message_type": message_type,
                "message_body": form.get("Body"),
                "media_id": media_url,
                "media_url": media_url,
                "media_content_type": media_content_type,
                "processing_status": "RECEIVED",
            }

            try:
                message = create_message(db, payload)
            except IntegrityError:
                db.rollback()
                message = get_message_by_id(db, message_id)

            if message and message_type == "audio" and media_url:
                background_tasks.add_task(
                    process_whatsapp_message,
                    message_id,
                )

    finally:
        db.close()

    # Immediate acknowledgement. Long-running Gemini processing happens
    # in the background so Twilio does not wait for AI processing.
    return _twiml_response(
        "Thank you. Your Civix grievance has been received and is being processed."
    )


@router.get("/whatsapp/messages")
def whatsapp_messages():
    """Development endpoint for inspecting received WhatsApp messages."""
    db = SessionLocal()
    try:
        from app.db.repositories.whatsapp_repository import get_messages
        return get_messages(db)
    finally:
        db.close()
