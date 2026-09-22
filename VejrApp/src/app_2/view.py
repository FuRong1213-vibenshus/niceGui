from nicegui import ui

import plotly.express as px
import plotly.graph_objects as go
from options import DATE_RANGE, DMI_OBSERVATION_URL, PARAMETERS, STATIONS


@ui.refreshable
def weather_view() -> None:
    ui.label("Weather App - Version 2 - MVVM architecture ").classes(
        "text-2xl font-bold"
    )
    fig = go.Figure()
    plot = ui.plotly(fig).classes("w-full h-96")

    with ui.row().classes("items-end"):
        station_select = ui.select(
            list(STATIONS.keys()),
            value="Copenhagen / Koebenhavn",
            label="Station",
        )
        parameter_select = ui.select(
            list(PARAMETERS.keys()),
            value="Temperature",
            label="Parameter",
        )

        ui.button("Load data", on_click=update_data)
