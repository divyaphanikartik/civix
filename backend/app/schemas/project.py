from typing import List

from pydantic import BaseModel


class ProjectConceptNote(BaseModel):

    project_title: str

    target_administrative_unit: str

    recommended_central_scheme: str

    estimated_capital_outlay_inr_lakhs: float

    estimated_beneficiaries: int

    executive_problem_statement: str

    socio_economic_impact_justification: str

    risk_and_feasibility_flags: List[str]

    preliminary_timeline_months: int