from google import genai
from google.genai import types

from app.config import settings
from app.schemas.grievance import CitizenGrievanceExtraction
from app.schemas.project import ProjectConceptNote


client = genai.Client(api_key=settings.GEMINI_API_KEY)


GRIEVANCE_INSTRUCTIONS = """
Extract the citizen grievance from the supplied message.

Translate it to English when necessary.

Extract:
- infrastructure sector
- asset type
- failure mode
- urgency
- spoken/written landmarks
- reported location

Do not invent information.

If the citizen explicitly mentions a locality, landmark, street, village,
colony, ward, town, or other place, use it as the incident location.
If no location is provided, leave the location fields empty rather than guessing.
"""


def extract_grievance_from_audio(audio_bytes: bytes):
    parts = [
        types.Part.from_bytes(
            data=audio_bytes,
            mime_type="audio/ogg",
        ),
        GRIEVANCE_INSTRUCTIONS,
    ]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=parts,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CitizenGrievanceExtraction,
            temperature=0.0,
        ),
    )

    return CitizenGrievanceExtraction.model_validate_json(response.text)


def extract_grievance_from_text(text: str):
    contents = [
        GRIEVANCE_INSTRUCTIONS,
        "Citizen message:\n" + text,
    ]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CitizenGrievanceExtraction,
            temperature=0.0,
        ),
    )

    return CitizenGrievanceExtraction.model_validate_json(response.text)


def generate_project_concept_note(prompt: str):
    response = client.models.generate_content(
        model="gemini-3.1-pro-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ProjectConceptNote,
            temperature=0.2,
        ),
    )

    return ProjectConceptNote.model_validate_json(response.text)
