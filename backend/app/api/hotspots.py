from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.hotspot import Hotspot
from app.schemas.hotspot import HotspotResponse


router = APIRouter(
    prefix="/hotspots",
    tags=["Hotspots"]
)


@router.get(
    "",
    response_model=list[HotspotResponse]
)
def get_hotspots(
    db: Session = Depends(get_db)
):

    return (
        db.query(Hotspot)
        .order_by(
            Hotspot.total_score.desc()
        )
        .all()
    )


@router.get(
    "/{hotspot_id}",
    response_model=HotspotResponse
)
def get_hotspot(
    hotspot_id: int,
    db: Session = Depends(get_db)
):

    return (
        db.query(Hotspot)
        .filter(
            Hotspot.id == hotspot_id
        )
        .first()
    )