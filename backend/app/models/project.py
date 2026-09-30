from sqlalchemy import Column, Integer, String, Float, Text
from app.db.database import Base


class ProjectConceptNote(Base):
    __tablename__ = "project_concept_notes"

    id = Column(Integer, primary_key=True)

    hotspot_id = Column(Integer)

    project_title = Column(String)

    target_administrative_unit = Column(String)

    recommended_central_scheme = Column(String)

    estimated_capital_outlay_inr_lakhs = Column(Float)

    estimated_beneficiaries = Column(Integer)

    executive_problem_statement = Column(Text)

    socio_economic_impact_justification = Column(Text)

    risk_and_feasibility_flags = Column(Text)

    preliminary_timeline_months = Column(Integer)