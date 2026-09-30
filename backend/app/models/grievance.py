from sqlalchemy import Column, Integer, String, Float, Text
from app.db.database import Base


class Grievance(Base):
    __tablename__ = "grievances"

    id = Column(Integer, primary_key=True)

    whatsapp_message_id = Column(String, unique=True)

    sender_phone = Column(String)

    detected_language = Column(String)

    english_translation = Column(Text)

    sector = Column(String)

    asset_type = Column(String)

    failure_mode = Column(Text)

    urgency = Column(String)

    reported_location_name = Column(String)

    incident_lat = Column(Float)
    incident_lon = Column(Float)

    reporter_lat = Column(Float)
    reporter_lon = Column(Float)

    confidence_score = Column(Float)

    status = Column(String, default="RECEIVED")