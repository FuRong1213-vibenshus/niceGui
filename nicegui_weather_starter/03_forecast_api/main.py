from nicegui import ui
import httpx
import pandas as pd
import plotly.express as px


DMI_FORECAST_URL = "https://opendataapi.dmi.dk/v1/forecastedr/collections/harmonie_dini_sf/position"


async def fetch_forecast(longitude: float, latitude: float) -> pd.DataFrame:
    """Fetch forecast data from DMI for one position."""
    params = {
        "coords": f"POINT({longitude} {latitude})",
        "crs": "crs84",
        "parameter-name": "temperature-2m",
        "f": "GeoJSON",
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(DMI_FORECAST_URL, params=params)
        response.raise_for_status()

    data = response.json()

    rows = []
    for feature in data["features"]:
        props = feature["properties"]
        rows.append(
            {
                "time": props["step"],
                "temperature": props["temperature-2m"] - 273.15,
            }
        )

    return pd.DataFrame(rows)


def make_forecast_plot(df: pd.DataFrame):
    return px.line(
        df,
        x="time",
        y="temperature",
        title="DMI forecast temperature",
        labels={"time": "Forecast time", "temperature": "Temperature, C"},
    )


async def load_forecast():
    # TODO: Add validation if the user writes text instead of numbers.
    lon = float(longitude_input.value)
    lat = float(latitude_input.value)

    df = await fetch_forecast(lon, lat)
    chart.figure = make_forecast_plot(df)
    chart.update()
    ui.notify("Forecast loaded")


ui.label("Weather App - Version 3").classes("text-2xl font-bold")
ui.label("This version uses async API calls with httpx.")

with ui.row().classes("items-end"):
    longitude_input = ui.input("Longitude", value="12.561")
    latitude_input = ui.input("Latitude", value="55.715")
    ui.button("Load forecast", on_click=load_forecast)

chart = ui.plotly(make_forecast_plot(pd.DataFrame({"time": [], "temperature": []}))).classes("w-full")

# TODO: Add a select menu with Copenhagen, Aarhus, Odense, and Aalborg.

ui.run()

