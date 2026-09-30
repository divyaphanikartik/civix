from pydantic import BaseModel


class HotspotResponse(BaseModel):

    id: int

    hotspot_code: str

    panchayat: str

    block: str

    district: str

    state: str

    latitude: float

    longitude: float

    sector: str

    complaints: int

    mpi_score: float

    demand_score: float
    equity_score: float
    deficit_score: float
    budget_score: float

    total_score: float

    dominant_issue: str

    status: str

    class Config:
        from_attributes = True