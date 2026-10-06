import pandas as pd
import requests


def fetch_coordinates(address: str) -> tuple[float, float]:
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": address,
        "count": 1,
        "language": "en",
        "format": "json",
        "countryCode": "DK",
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=(5, 10),
        )
        response.raise_for_status()

    except requests.Timeout as error:
        raise RuntimeError("The coordinate request timed out.") from error

    except requests.ConnectionError as error:
        raise RuntimeError("Could not connect to the geocoding service.") from error

    except requests.HTTPError as error:
        raise RuntimeError(
            f"Geocoding returned HTTP {response.status_code}."
        ) from error

    data = response.json()
    results = data.get("results", [])

    if not results:
        raise ValueError(f"No coordinates were found for {address!r}.")

    location = results[0]

    return (
        float(location["latitude"]),
        float(location["longitude"]),
    )


def fetch_forecast(
    address: str,
    parameter: str,
    forecast_days: int,
):
    lat, lon = fetch_coordinates(address=address)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": [parameter, "precipitation"],
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
        ],
        "forecast_days": forecast_days,
        "timezone": "Europe/Copenhagen",
        "models": "dmi_seamless",
    }
    print("waiting for response", flush=True)

    response = requests.get(
        url,
        params=params,
        timeout=10,
    )
    response.raise_for_status()
    print("Response received", flush=True)
    data = response.json()
    print(data)
    # Each key in data["hourly"] is a list, so it becomes a column in the DataFrame.
    hourly_dataframe = pd.DataFrame(data["hourly"])
    hourly_dataframe = hourly_dataframe.rename(columns={"time": "date"})
    hourly_dataframe["date"] = pd.to_datetime(hourly_dataframe["date"])

    daily_dataframe = pd.DataFrame(data["daily"])
    daily_dataframe = daily_dataframe.rename(columns={"time": "date"})
    daily_dataframe["date"] = pd.to_datetime(daily_dataframe["date"])

    return hourly_dataframe, daily_dataframe


if __name__ == "__main__":
    print(fetch_coordinates("Copenhagen"))
    print(fetch_forecast("Copenhagen", "temperature_2m", 3))
