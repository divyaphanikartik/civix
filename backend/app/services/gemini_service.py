from google import genai
from google.genai import types

from app.config import settings
from app.schemas.grievance import CitizenGrievanceExtraction
from app.schemas.project import ProjectConceptNote


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def extract_grievance_from_audio(
    audio_bytes: bytes
):

    instructions = """
    Transcribe the citizen's spoken complaint.

    Translate it to English.

    Extract:
    - infrastructure sector
    - asset type
    - failure mode
    - urgency
    - spoken landmarks
    - reported location

    Do not invent information.

    If the citizen explicitly mentions
    a locality, use that locality as
    the incident location.
    """

    parts = [
        types.Part.from_bytes(
            data=audio_bytes,
            mime_type="audio/ogg"
        ),
        instructions
    ]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=parts,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CitizenGrievanceExtraction,
            temperature=0.0
        )
    )

    return CitizenGrievanceExtraction.model_validate_json(
        response.text
    )


def generate_project_concept_note(
    prompt: str
):

    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ProjectConceptNote,
            temperature=0.2
        )
    )

    return ProjectConceptNote.model_validate_json(
        response.text
    )