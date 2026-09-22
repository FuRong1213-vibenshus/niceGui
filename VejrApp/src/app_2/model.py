import openmeteo_requests

import pandas as pd
from dataclasses import dataclass, field
import requests_cache
from retry_requests import retry


# Setup the Open-Meteo API client with cache and retry on error


def fetch_forecast(city: str, parameter: str):
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(
        session=retry_session,  # pyright: ignore[reportArgumentType]
    )

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 52.52,
        "longitude": 13.41,
        "hourly": "temperature_2m",
        "forecast_days": 3,
        "models": "dmi_seamless",
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()

    if hourly is None:
        raise ValueError("No hourly weather data was returned by Open-Meteo.")

    hourly_temperature_2m_var = hourly.Variables(0)

    if hourly_temperature_2m_var is None:
        raise ValueError("No temperature data was returned by Open-Meteo.")

    hourly_temperature_2m = hourly_temperature_2m_var.ValuesAsNumpy()

    hourly_dataframe = pd.DataFrame(
        {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left",
            ),
            "temperature_2m": hourly_temperature_2m,
        }
    )
    return hourly_dataframe
