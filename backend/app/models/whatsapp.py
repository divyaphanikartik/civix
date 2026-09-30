from sqlalchemy import Column, Integer, String, Text

from app.db.database import Base


class WhatsAppMessage(Base):
    __tablename__ = "whatsapp_messages"

    id = Column(Integer, primary_key=True)

    # Twilio message SID (e.g. SM...)
    message_id = Column(String, unique=True, nullable=False, index=True)

    sender_phone = Column(String, nullable=False, index=True)

    recipient_phone = Column(String)

    message_type = Column(String, nullable=False)

    message_body = Column(Text)

    media_id = Column(String)

    media_url = Column(Text)

    media_content_type = Column(String)

    processing_status = Column(
        String,
        default="RECEIVED",
        nullable=False,
        index=True,
    )

    error_message = Column(Text)
