import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Twilio WhatsApp Sandbox / WhatsApp provider
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_WHATSAPP_NUMBER = os.getenv(
        "TWILIO_WHATSAPP_NUMBER",
        "whatsapp:+14155238886",
    )
    TWILIO_VALIDATE_WEBHOOK_SIGNATURE = os.getenv(
        "TWILIO_VALIDATE_WEBHOOK_SIGNATURE",
        "false",
    ).lower() == "true"

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://civix:civix@localhost:5432/civix",
    )

    FRONTEND_URL = os.getenv(
        "FRONTEND_URL",
        "http://localhost:5173",
    )


settings = Settings()
