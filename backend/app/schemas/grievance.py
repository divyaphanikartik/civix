from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class InfrastructureSector(str, Enum):

    ROADS_BRIDGES = "Roads & Bridges"

    WATER_SANITATION = "Water & Sanitation"

    POWER_ENERGY = "Power & Energy"

    HEALTHCARE = "Primary Healthcare"

    EDUCATION = "Education Infrastructure"

    DRAINAGE_FLOOD = "Drainage & Flood Control"


class UrgencyLevel(str, Enum):

    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class CitizenGrievanceExtraction(BaseModel):

    detected_language: str

    english_translation: str

    sector: InfrastructureSector

    asset_type: str

    failure_mode: str

    urgency: UrgencyLevel

    landmark_entities: List[str]

    reported_location_name: str

    visual_evidence_analysis: Optional[str] = None

    confidence_score: float = Field(
        ge=0.0,
        le=1.0
    )