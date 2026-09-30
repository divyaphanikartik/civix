from typing import Optional

from sqlalchemy.orm import Session

from app.models.hotspot import Hotspot


def create_hotspot(
    db: Session,
    payload: dict,
    *,
    commit: bool = True,
):
    hotspot = Hotspot(**payload)

    db.add(hotspot)
    db.flush()

    if commit:
        db.commit()
        db.refresh(hotspot)

    return hotspot


def get_hotspot(
    db: Session,
    hotspot_id: int,
):
    return (
        db.query(Hotspot)
        .filter(Hotspot.id == hotspot_id)
        .first()
    )


def get_hotspots(
    db: Session,
    *,
    sector: Optional[str] = None,
    minimum_score: float = 0.0,
    limit: int = 500,
):
    query = db.query(Hotspot)

    if sector:
        query = query.filter(
            Hotspot.sector == sector
        )

    query = query.filter(
        Hotspot.total_score >= minimum_score
    )

    return (
        query
        .order_by(Hotspot.total_score.desc())
        .limit(limit)
        .all()
    )


def update_hotspot(
    db: Session,
    hotspot,
    values: dict,
):
    for key, value in values.items():
        setattr(hotspot, key, value)

    db.commit()
    db.refresh(hotspot)

    return hotspot


def delete_hotspot(
    db: Session,
    hotspot,
):
    db.delete(hotspot)
    db.commit()