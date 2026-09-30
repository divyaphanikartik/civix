from sqlalchemy import Column, Integer, String, Float, Text
from app.db.database import Base


class Hotspot(Base):
    __tablename__ = "hotspots"

    id = Column(Integer, primary_key=True)

    hotspot_code = Column(String, unique=True)

    lgd_code = Column(String)

    panchayat = Column(String)
    block = Column(String)
    district = Column(String)
    state = Column(String)

    latitude = Column(Float)
    longitude = Column(Float)

    sector = Column(String)

    complaints = Column(Integer, default=0)

    critical_complaints = Column(Integer, default=0)

    mpi_score = Column(Float)

    tribal_population_pct = Column(Float)

    total_population = Column(Integer)

    distance_to_nearest_facility_km = Column(Float)

    sanctioned_budget_lakhs = Column(Float)

    scheme_name = Column(String)

    dominant_issue = Column(Text)

    demand_score = Column(Float)
    equity_score = Column(Float)
    deficit_score = Column(Float)
    budget_score = Column(Float)

    total_score = Column(Float)

    status = Column(String)