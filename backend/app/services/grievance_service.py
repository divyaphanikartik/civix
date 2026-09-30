from app.services.gemini_service import (
    extract_grievance_from_audio
)

from app.services.geolocation_service import (
    forward_geocode
)

from app.services.mcda_service import (
    calculate_mcda_score
)


def process_voice_grievance(
    audio_bytes: bytes,
    reporter_lat: float | None = None,
    reporter_lon: float | None = None
):

    # 1. Gemini extraction

    grievance = extract_grievance_from_audio(
        audio_bytes
    )

    # 2. Resolve incident location

    incident_lat = None
    incident_lon = None

    if grievance.landmark_entities:

        landmark = (
            grievance.landmark_entities[0]
        )

        coordinates = forward_geocode(
            landmark
        )

        if coordinates:

            incident_lat, incident_lon = coordinates

    # 3. Fall back to reporter location

    if incident_lat is None:

        incident_lat = reporter_lat
        incident_lon = reporter_lon

    # 4. Find public data

    # TODO:
    # Retrieve actual block/MPI/
    # infrastructure/budget information.

    # 5. Calculate MCDA

    score = calculate_mcda_score(
        complaints=1,
        mpi=0.0,
        distance_km=4.2,
        budget_lakhs=0.0
    )

    # 6. Persist grievance/hotspot

    # TODO

    return {
        "grievance": grievance,
        "incident_lat": incident_lat,
        "incident_lon": incident_lon,
        "score": score
    }