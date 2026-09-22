from nicegui import ui
import pandas as pd
import plotly.express as px
import requests


DMI_OBSERVATION_URL = (
    "https://opendataapi.dmi.dk/v2/metObs/collections/observation/items"
)


def fetch_observations(station_id: str, parameter_id: str) -> pd.DataFrame:
    """Fetch measured observation data from DMI Frie Data."""
    params = {
        "stationId": station_id,
        "parameterId": parameter_id,
        "datetime": "2018-02-12T00:00:00Z/2018-02-13T00:00:00Z",
        "limit": 100,
        "sortorder": "observed,ASC",
    }

    response = requests.get(DMI_OBSERVATION_URL, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()

    rows = []
    for feature in data["features"]:
        props = feature["properties"]
        rows.append(
            {
                "time": props["observed"],
                "value": props["value"],
                "parameter": props["parameterId"],
            }
        )

    return pd.DataFrame(rows)


def make_plot(df: pd.DataFrame, parameter_id: str):
    return px.line(
        df,
        x="time",
        y="value",
        title=f"DMI observation: {parameter_id}",
        labels={"time": "Time", "value": parameter_id},
    )


async def load_data():
    station_id = station_input.value
    parameter_id = parameter_select.value

    # TODO: Validate that station_id is not empty.
    df = fetch_observations(station_id, parameter_id)

    chart.figure = make_plot(df, parameter_id)
    chart.update()
    ui.notify("Data loaded")


ui.label("Weather App - Version 2").classes("text-2xl font-bold")
ui.label("This version fetches measured observations from DMI.")

with ui.row().classes("items-end"):
    station_input = ui.input("Station ID", value="06149")
    parameter_select = ui.select(
        ["temp_dry", "humidity", "wind_speed"],
        value="temp_dry",
        label="Parameter",
    )
    ui.button("Load data", on_click=load_data)

empty_df = pd.DataFrame({"time": [], "value": []})
chart = ui.plotly(make_plot(empty_df, "temp_dry")).classes("w-full")


# TODO: Add error handling with try/except around the API call.

ui.run()
