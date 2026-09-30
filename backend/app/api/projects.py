import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.project_service import create_concept_note


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post("/concept-note/{hotspot_id}")
def generate_concept_note(
    hotspot_id: int,
    db: Session = Depends(get_db),
):
    project = create_concept_note(
        db,
        hotspot_id,
    )

    return {
        "id": project.id,
        "hotspot_id": project.hotspot_id,
        "project_title": project.project_title,
        "target_administrative_unit": (
            project.target_administrative_unit
        ),
        "recommended_central_scheme": (
            project.recommended_central_scheme
        ),
        "estimated_capital_outlay_inr_lakhs": (
            project.estimated_capital_outlay_inr_lakhs
        ),
        "estimated_beneficiaries": (
            project.estimated_beneficiaries
        ),
        "executive_problem_statement": (
            project.executive_problem_statement
        ),
        "socio_economic_impact_justification": (
            project.socio_economic_impact_justification
        ),
        "risk_and_feasibility_flags": json.loads(
            project.risk_and_feasibility_flags
        )
        if project.risk_and_feasibility_flags
        else [],
        "preliminary_timeline_months": (
            project.preliminary_timeline_months
        ),
    }