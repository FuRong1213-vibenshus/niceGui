from nicegui import ui

import plotly.graph_objects as go
import plotly.express as px
from options import PARAMETERS, STATIONS
from viewmodel import WeatherViewModel

vm = WeatherViewModel()
fig = go.Figure()
fig.add_trace(go.Scatter(name="forcast"))
plot = None


def weather_view() -> None:

    global plot
    ui.label("Weather App - Version 2 - MVVM architecture ").classes(
        "text-2xl font-bold"
    )
    with ui.grid(columns=2).classes("w-full gap-4"):
        with ui.card().classes("w-full"):
            ui.label("City Selection")
            ui.select(
                options=list(STATIONS),
                value="Copenhagen",
                label="Station",
            ).bind_value_to(vm.state, "city")
        with ui.card().classes("w-full"):
            ui.label("Weather Parameter")
            ui.select(
                list(PARAMETERS.keys()),
                value="temperature_2m",
                label="Parameter",
            ).bind_value_to(vm.state, "parameter")

    ui.button("Update", on_click=show_plot)
    plot = ui.plotly(fig).classes("w-full h-96")


def update_figure():
    df = vm.state.temp_forecast
    fig.update_traces(x=df["date"], y=df["temperature_2m"])
    if plot is not None:
        plot.update()


def show_plot():
    try:
        vm.load_temp_forecast()
    except Exception as error:
        ui.notify(
            f"Could not fetch weather data:{error}",
            type="negative",
        )
        return
    try:
        update_figure()
    except Exception as error:
        print(repr(error))
        ui.notify(f"Could not update figure: {error}", type="negative")


weather_view()

ui.run()
