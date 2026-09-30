import json
from sqlalchemy.orm import Session

from app.db.repositories.hotspot_repository import (
    get_hotspot,
)

from app.db.repositories.project_repository import (
    create_project,
)

from app.services.gemini_service import (
    generate_project_concept_note,
)


def build_concept_note_prompt(hotspot):
    return f"""
You are preparing a preliminary government infrastructure
Project Concept Note based on a Civix citizen grievance hotspot.

Hotspot:
- Code: {hotspot.hotspot_code}
- State: {hotspot.state}
- District: {hotspot.district}
- Block: {hotspot.block}
- Panchayat: {hotspot.panchayat}
- Sector: {hotspot.sector}
- Dominant issue: {hotspot.dominant_issue}
- Complaints: {hotspot.complaints}
- Critical complaints: {hotspot.critical_complaints}
- MPI: {hotspot.mpi_score}
- Population: {hotspot.total_population}
- Tribal percentage: {hotspot.tribal_population_pct}
- Distance to facility: {hotspot.distance_to_nearest_facility_km} km
- Existing budget: ₹{hotspot.sanctioned_budget_lakhs} lakhs
- Recommended scheme: {hotspot.scheme_name}

MCDA:
- Demand score: {hotspot.demand_score}/30
- Equity score: {hotspot.equity_score}/30
- Deficit score: {hotspot.deficit_score}/25
- Budget score: {hotspot.budget_score}/15
- Total score: {hotspot.total_score}/100

Prepare a preliminary Project Concept Note.

Do not invent specific government approvals,
sanctions, financial allocations, or verified statistics.

Clearly distinguish preliminary estimates from
verified government data.
"""


def create_concept_note(
    db: Session,
    hotspot_id: int,
):
    hotspot = get_hotspot(db, hotspot_id)

    if not hotspot:
        raise ValueError(
            f"Hotspot {hotspot_id} not found"
        )

    prompt = build_concept_note_prompt(hotspot)

    concept = generate_project_concept_note(prompt)

    payload = {
        "hotspot_id": hotspot.id,
        "project_title": concept.project_title,
        "target_administrative_unit": (
            concept.target_administrative_unit
        ),
        "recommended_central_scheme": (
            concept.recommended_central_scheme
        ),
        "estimated_capital_outlay_inr_lakhs": (
            concept.estimated_capital_outlay_inr_lakhs
        ),
        "estimated_beneficiaries": (
            concept.estimated_beneficiaries
        ),
        "executive_problem_statement": (
            concept.executive_problem_statement
        ),
        "socio_economic_impact_justification": (
            concept.socio_economic_impact_justification
        ),
        "risk_and_feasibility_flags": json.dumps(
            concept.risk_and_feasibility_flags
        ),
        "preliminary_timeline_months": (
            concept.preliminary_timeline_months
        ),
    }

    return create_project(db, payload)