from typing import Optional

from pydantic import BaseModel


class HotspotResponse(BaseModel):
    id: int
    hotspot_code: str
    panchayat: Optional[str] = None
    block: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    sector: str
    complaints: int
    mpi_score: Optional[float] = 0.0
    demand_score: Optional[float] = 0.0
    equity_score: Optional[float] = 0.0
    deficit_score: Optional[float] = 0.0
    budget_score: Optional[float] = 0.0
    total_score: Optional[float] = 0.0
    dominant_issue: Optional[str] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True
