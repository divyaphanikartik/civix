import json
import urllib.parse
import urllib.request


USER_AGENT = "Civix/1.0"


def reverse_geocode(
    latitude: float,
    longitude: float
):
    url = (
        "https://nominatim.openstreetmap.org/"
        f"reverse?format=jsonv2"
        f"&lat={latitude}"
        f"&lon={longitude}"
    )

    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT}
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=5
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

        address = data.get("address", {})

        suburb = (
            address.get("suburb")
            or address.get("neighbourhood")
            or address.get("residential")
            or address.get("road")
        )

        district = (
            address.get("city")
            or address.get("state_district")
            or address.get("county")
        )

        state = address.get("state")

        if suburb and district and state:
            return f"{suburb}, {district}, {state}"

    except Exception:
        pass

    return None


def forward_geocode(place_query: str):

    query = f"{place_query}, India"

    encoded = urllib.parse.quote(query)

    url = (
        "https://nominatim.openstreetmap.org/"
        f"search?format=json"
        f"&q={encoded}"
        f"&limit=1"
    )

    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT}
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=5
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

        if data:
            return (
                float(data[0]["lat"]),
                float(data[0]["lon"])
            )

    except Exception:
        pass

    return None