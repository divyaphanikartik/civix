from typing import Optional

from sqlalchemy.orm import Session

from app.db.repositories.hotspot_repository import (
    create_hotspot,
    get_hotspot,
    get_hotspots,
    update_hotspot,
)
from app.services.mcda_service import calculate_mcda_score


def calculate_hotspot_scores(
    complaints: int,
    mpi: float,
    distance_km: float,
    budget_lakhs: float,
):
    return calculate_mcda_score(
        complaints=complaints,
        mpi=mpi,
        distance_km=distance_km,
        budget_lakhs=budget_lakhs,
    )


def build_hotspot_payload(
    *,
    hotspot_code: Optional[str],
    state: Optional[str],
    district: Optional[str],
    block: Optional[str],
    panchayat: Optional[str],
    latitude: Optional[float],
    longitude: Optional[float],
    sector: str,
    complaints: int,
    critical_complaints: int = 0,
    mpi: float = 0.0,
    tribal_percentage: float = 0.0,
    population: int = 0,
    distance_to_facility_km: float = 0.0,
    budget_lakhs: float = 0.0,
    recommended_scheme: Optional[str] = None,
    dominant_issue: Optional[str] = None,
    lgd_code: Optional[str] = None,
):
    scores = calculate_hotspot_scores(
        complaints=complaints,
        mpi=mpi,
        distance_km=distance_to_facility_km,
        budget_lakhs=budget_lakhs,
    )

    return {
        "hotspot_code": hotspot_code,
        "lgd_code": lgd_code,
        "panchayat": panchayat,
        "block": block,
        "district": district,
        "state": state,
        "latitude": latitude,
        "longitude": longitude,
        "sector": sector,
        "complaints": complaints,
        "critical_complaints": critical_complaints,
        "mpi_score": mpi,
        "tribal_population_pct": tribal_percentage,
        "total_population": population,
        "distance_to_nearest_facility_km": distance_to_facility_km,
        "sanctioned_budget_lakhs": budget_lakhs,
        "scheme_name": recommended_scheme,
        "dominant_issue": dominant_issue,
        "demand_score": scores["demand"],
        "equity_score": scores["equity"],
        "deficit_score": scores["deficit"],
        "budget_score": scores["budget"],
        "total_score": scores["total"],
        "status": "ACTIVE",
    }


def create_hotspot_from_grievance(
    db: Session,
    *,
    location: dict,
    grievance,
    public_data: Optional[dict] = None,
):
    public_data = public_data or {}

    payload = build_hotspot_payload(
        hotspot_code=None,
        lgd_code=location.get("lgd_code"),
        state=location.get("state"),
        district=location.get("district"),
        block=location.get("block"),
        panchayat=location.get("panchayat"),
        latitude=location.get("latitude"),
        longitude=location.get("longitude"),
        sector=grievance.sector,
        complaints=public_data.get("complaints", 1),
        critical_complaints=public_data.get("critical_complaints", 0),
        mpi=public_data.get("mpi", 0.0),
        tribal_percentage=public_data.get("tribal_percentage", 0.0),
        population=public_data.get("population", 0),
        distance_to_facility_km=public_data.get("distance_to_facility_km", 4.2),
        budget_lakhs=public_data.get("budget_lakhs", 0.0),
        recommended_scheme=public_data.get("recommended_scheme"),
        dominant_issue=grievance.failure_mode,
    )

    existing = get_hotspots(db, limit=10000)
    payload["hotspot_code"] = f"HS-{len(existing) + 1:03d}"
    return create_hotspot(db, payload)


def list_hotspots(
    db: Session,
    *,
    sector: Optional[str] = None,
    minimum_score: float = 0.0,
):
    hotspots = get_hotspots(
        db,
        sector=sector,
        minimum_score=minimum_score,
    )
    return sorted(
        hotspots,
        key=lambda item: item.total_score or 0,
        reverse=True,
    )


def get_hotspot_by_id(db: Session, hotspot_id: int):
    return get_hotspot(db, hotspot_id)


def update_hotspot_score(db: Session, hotspot):
    scores = calculate_hotspot_scores(
        complaints=hotspot.complaints or 0,
        mpi=hotspot.mpi_score or 0.0,
        distance_km=hotspot.distance_to_nearest_facility_km or 0.0,
        budget_lakhs=hotspot.sanctioned_budget_lakhs or 0.0,
    )

    return update_hotspot(
        db,
        hotspot,
        {
            "demand_score": scores["demand"],
            "equity_score": scores["equity"],
            "deficit_score": scores["deficit"],
            "budget_score": scores["budget"],
            "total_score": scores["total"],
        },
    )
