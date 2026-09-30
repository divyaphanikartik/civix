import math
from typing import Optional

from sqlalchemy.orm import Session

from app.db.repositories.grievance_repository import (
    create_grievance,
    get_grievance_by_whatsapp_message_id,
)
from app.db.repositories.hotspot_repository import (
    create_hotspot,
    get_hotspots,
    update_hotspot,
)
from app.services.geolocation_service import (
    forward_geocode_details,
)
from app.services.mcda_service import calculate_mcda_score
from app.services.gemini_service import (
    extract_grievance_from_audio,
    extract_grievance_from_text,
)
from app.services.hotspot_service import build_hotspot_payload


HOTSPOT_MERGE_RADIUS_KM = 1.0


def _urgency_value(urgency) -> str:
    return getattr(urgency, "value", str(urgency))


def _resolve_location(grievance):
    candidates = []

    for landmark in grievance.landmark_entities or []:
        if landmark and landmark.strip():
            candidates.append(landmark.strip())

    if grievance.reported_location_name:
        candidates.append(grievance.reported_location_name.strip())

    for candidate in candidates:
        details = forward_geocode_details(candidate)
        if details:
            return details

    return {
        "latitude": None,
        "longitude": None,
        "display_name": grievance.reported_location_name or None,
        "state": None,
        "district": None,
        "block": None,
        "panchayat": None,
        "lgd_code": None,
    }


def _distance_km(lat1, lon1, lat2, lon2):
    if None in (lat1, lon1, lat2, lon2):
        return None

    radius = 6371.0
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)

    a = (
        math.sin(dp / 2) ** 2
        + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    )
    return radius * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _find_matching_hotspot(db: Session, grievance, location):
    candidates = get_hotspots(db, sector=grievance.sector, limit=500)

    for hotspot in candidates:
        distance = _distance_km(
            location.get("latitude"),
            location.get("longitude"),
            hotspot.latitude,
            hotspot.longitude,
        )
        if distance is not None and distance <= HOTSPOT_MERGE_RADIUS_KM:
            return hotspot

    return None


def _create_or_update_hotspot(
    db: Session,
    *,
    grievance,
    location: dict,
):
    existing = _find_matching_hotspot(db, grievance, location)

    if existing:
        complaints = (existing.complaints or 0) + 1
        critical = (existing.critical_complaints or 0) + (
            1 if _urgency_value(grievance.urgency).upper() == "CRITICAL" else 0
        )

        scores = calculate_mcda_score(
            complaints=complaints,
            mpi=existing.mpi_score or 0.0,
            distance_km=existing.distance_to_nearest_facility_km or 4.2,
            budget_lakhs=existing.sanctioned_budget_lakhs or 0.0,
        )

        return update_hotspot(
            db,
            existing,
            {
                "complaints": complaints,
                "critical_complaints": critical,
                "dominant_issue": grievance.failure_mode,
                "demand_score": scores["demand"],
                "equity_score": scores["equity"],
                "deficit_score": scores["deficit"],
                "budget_score": scores["budget"],
                "total_score": scores["total"],
            },
        )

    payload = build_hotspot_payload(
        hotspot_code=None,
        state=location.get("state") or "Unknown",
        district=location.get("district") or location.get("display_name") or "Unknown",
        block=location.get("block"),
        panchayat=location.get("panchayat") or grievance.reported_location_name,
        latitude=location.get("latitude"),
        longitude=location.get("longitude"),
        sector=grievance.sector,
        complaints=1,
        critical_complaints=(
            1 if _urgency_value(grievance.urgency).upper() == "CRITICAL" else 0
        ),
        mpi=0.0,
        tribal_percentage=0.0,
        population=0,
        distance_to_facility_km=4.2,
        budget_lakhs=0.0,
        recommended_scheme=None,
        dominant_issue=grievance.failure_mode,
        lgd_code=location.get("lgd_code"),
    )

    # Generate the code after checking existing rows. The worker is single-threaded,
    # so this is deterministic for the current prototype.
    existing_count = len(get_hotspots(db, limit=10000))
    payload["hotspot_code"] = f"HS-{existing_count + 1:03d}"

    return create_hotspot(db, payload, commit=False)


def _persist_result(
    db: Session,
    *,
    message,
    grievance,
    location: dict,
):
    existing = get_grievance_by_whatsapp_message_id(
        db,
        message.message_id,
    )
    if existing:
        return existing, _find_matching_hotspot(db, grievance, location)

    grievance_row = create_grievance(
        db,
        {
            "whatsapp_message_id": message.message_id,
            "sender_phone": message.sender_phone,
            "detected_language": grievance.detected_language,
            "english_translation": grievance.english_translation,
            "sector": grievance.sector,
            "asset_type": grievance.asset_type,
            "failure_mode": grievance.failure_mode,
            "urgency": _urgency_value(grievance.urgency),
            "reported_location_name": grievance.reported_location_name,
            "incident_lat": location.get("latitude"),
            "incident_lon": location.get("longitude"),
            "reporter_lat": None,
            "reporter_lon": None,
            "confidence_score": grievance.confidence_score,
            "status": "OPEN",
        },
        commit=False,
    )

    hotspot = _create_or_update_hotspot(
        db,
        grievance=grievance,
        location=location,
    )

    db.commit()
    db.refresh(grievance_row)
    db.refresh(hotspot)

    return grievance_row, hotspot


def process_grievance(
    db: Session,
    *,
    message,
    grievance,
):
    location = _resolve_location(grievance)
    grievance_row, hotspot = _persist_result(
        db,
        message=message,
        grievance=grievance,
        location=location,
    )

    return {
        "grievance": grievance_row,
        "hotspot": hotspot,
        "incident_lat": location.get("latitude"),
        "incident_lon": location.get("longitude"),
        "score": hotspot.total_score if hotspot else None,
    }


def process_voice_grievance(
    audio_bytes: bytes,
    db: Session,
    message,
):
    grievance = extract_grievance_from_audio(audio_bytes)
    return process_grievance(
        db,
        message=message,
        grievance=grievance,
    )


def process_text_grievance(
    text: str,
    db: Session,
    message,
):
    grievance = extract_grievance_from_text(text)
    return process_grievance(
        db,
        message=message,
        grievance=grievance,
    )
