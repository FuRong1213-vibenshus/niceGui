import pandas as pd
import openmeteo_requests
import requests_cache
from retry_requests import retry


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

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
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

    responses = openmeteo.weather_api(
        url,
        params=params,
        timeout=10,
    )
    print("Response received", flush=True)
    response = responses[0]
    # Process first location. Add a for-loop for multiple locations or weather models
    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["precipitation"] = hourly_precipitation

    hourly_dataframe = pd.DataFrame(data=hourly_data)

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()

    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left",
        )
    }

    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min

    daily_dataframe = pd.DataFrame(data=daily_data)
    return hourly_dataframe, daily_dataframe


if __name__ == "__main__":
    print(fetch_coordinates("Copenhagen"))
    print(fetch_forecast("Copenhagen", "temperature_2m", 3))
