import json
import urllib.parse
import urllib.request


USER_AGENT = "Civix/1.0"


def reverse_geocode(latitude: float, longitude: float):
    url = (
        "https://nominatim.openstreetmap.org/"
        f"reverse?format=jsonv2&lat={latitude}&lon={longitude}"
    )

    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))

        address = data.get("address", {})
        suburb = (
            address.get("suburb")
            or address.get("neighbourhood")
            or address.get("residential")
            or address.get("road")
        )
        district = (
            address.get("city")
            or address.get("town")
            or address.get("municipality")
            or address.get("state_district")
            or address.get("county")
        )
        state = address.get("state")

        if suburb and district and state:
            return f"{suburb}, {district}, {state}"
    except Exception:
        pass

    return None


def forward_geocode_details(place_query: str):
    if not place_query or not place_query.strip():
        return None

    query = f"{place_query.strip()}, India"
    encoded = urllib.parse.quote(query)
    url = (
        "https://nominatim.openstreetmap.org/"
        f"search?format=json&addressdetails=1&q={encoded}&limit=1"
    )

    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            data = json.loads(response.read().decode("utf-8"))

        if not data:
            return None

        item = data[0]
        address = item.get("address", {})

        return {
            "latitude": float(item["lat"]),
            "longitude": float(item["lon"]),
            "display_name": item.get("display_name"),
            "state": address.get("state"),
            "district": (
                address.get("city")
                or address.get("town")
                or address.get("municipality")
                or address.get("county")
                or address.get("state_district")
            ),
            "block": address.get("town") or address.get("municipality"),
            "panchayat": (
                address.get("village")
                or address.get("suburb")
                or address.get("neighbourhood")
            ),
            "lgd_code": None,
        }
    except Exception:
        return None


def forward_geocode(place_query: str):
    details = forward_geocode_details(place_query)
    if details:
        return details["latitude"], details["longitude"]
    return None
