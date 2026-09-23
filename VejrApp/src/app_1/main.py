import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from nicegui import ui


def make_weather_table() -> pd.DataFrame:
    """Return fake weather data for the first app version."""
    return pd.DataFrame(
        {
            "day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "temperature": [12, 14, 13, 16, 15],
            "rain": [0.0, 1.5, 0.2, 0.0, 3.1],
        }
    )


def make_weather_plot(
    df: pd.DataFrame,
    parameter: str,
) -> go.Figure:
    """
    Create a graph for the selected weather parameter.
    """
    if parameter == "temperature":
        title = "Temperature this week"
        y_label = "Temperature (°C)"
    else:
        title = "Rain this week"
        y_label = "Rain (mm)"

    return px.line(
        df,
        x="day",
        y=parameter,
        markers=True,
        title=title,
        labels={
            "day": "Day",
            parameter: y_label,
        },
    )


weather_data = make_weather_table()


def update_plot(parameter: str) -> None:
    plot.figure = make_weather_plot(weather_data, parameter)
    plot.update()


ui.label("Weather App").classes("text-2xl, font-bold")
ui.label("Version 1 - UI basis").classes("text-gray-500")

with ui.row():
    ui.button("Temperature", on_click=lambda: update_plot("temperature"))

    ui.button("Rain", on_click=lambda: update_plot("rain"))

plot = ui.plotly(make_weather_plot(weather_data, "temperature")).classes("w-full")

ui.run()
