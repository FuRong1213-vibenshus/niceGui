from nicegui import ui
import pandas as pd
import requests


def fetch_observations(station_id: str, parameter_id: str) -> pd.DataFrame:
    """Fetch measured observation data from DMI Frie Data."""
    params = {
        "stationId": station_id,
        "parameterId": parameter_id,
        "datetime": DATE_RANGE,
        "limit": 100,
    }

    response = requests.get(DMI_OBSERVATION_URL, params=params, timeout=20)

    # TODO:
    # 1. Tilføj error handling try/except omkring API kaldelsen i funktionen fetch_observations.
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


def update_data():
    station_id = STATIONS[station_select.value]
    parameter_id = PARAMETERS[parameter_select.value]

    # TODO: Show the chosen station ID somewhere in the UI.
    df = fetch_observations(station_id, parameter_id)

    new_fig = make_plot(df, parameter_id=parameter_id)
    plot.figure = new_fig
    plot.update()
    ui.notify("Data loaded")


ui.run()
