import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen


def fetch_coordinates(address: str) -> tuple[float, float]:
    params = urlencode(
        {
            "text": address,
            "format": "json",
            "limit": 1,
            "apiKey": "b011a14a23b547babff0f84259d3c38a",
        }
    )

    url = f"https://api.geoapify.com/v1/geocode/search?{params}"

    try:
        with urlopen(url, timeout=10) as response:
            data = json.load(response)

    except HTTPError as error:
        details = error.read().decode()
        raise RuntimeError(f"Geoapify returned HTTP {error.code}: {details}") from error

    except URLError as error:
        raise RuntimeError(f"Could not connect to Geoapify: {error.reason}") from error

    if not data.get("results"):
        raise ValueError(f"No coordinates found for {address!r}")

    result = data["results"][0]
    return float(result["lat"]), float(result["lon"])


print(fetch_coordinates("Copenhagen, Denmark"))
