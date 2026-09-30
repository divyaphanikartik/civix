import logging

import requests
from twilio.request_validator import RequestValidator
from twilio.rest import Client

from app.config import settings

logger = logging.getLogger(__name__)


def get_twilio_client():
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        raise RuntimeError(
            "TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN are required."
        )

    return Client(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN,
    )


def validate_webhook_signature(
    url: str,
    params: dict,
    signature: str | None,
) -> bool:
    if not settings.TWILIO_VALIDATE_WEBHOOK_SIGNATURE:
        return True

    if not signature or not settings.TWILIO_AUTH_TOKEN:
        return False

    validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
    return validator.validate(url, params, signature)


def download_media(media_url: str) -> bytes:
    """Download inbound WhatsApp media from Twilio."""
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        raise RuntimeError(
            "Twilio credentials are required to download media."
        )

    response = requests.get(
        media_url,
        auth=(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN,
        ),
        timeout=60,
    )
    response.raise_for_status()
    return response.content


def send_whatsapp_message(to_number: str, body: str):
    """Send a text response through the Twilio WhatsApp Sandbox."""
    client = get_twilio_client()

    destination = to_number
    if not destination.startswith("whatsapp:"):
        destination = f"whatsapp:{destination}"

    message = client.messages.create(
        body=body,
        from_=settings.TWILIO_WHATSAPP_NUMBER,
        to=destination,
    )

    logger.info(
        "Twilio WhatsApp message sent: sid=%s to=%s",
        message.sid,
        destination,
    )

    return message
