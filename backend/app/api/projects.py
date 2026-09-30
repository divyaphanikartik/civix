from fastapi import APIRouter

from app.services.project_service import (
    create_concept_note
)


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post(
    "/concept-note/{hotspot_id}"
)
def generate_concept_note(
    hotspot_id: int
):

    return create_project_concept_note(
        hotspot_id
    )