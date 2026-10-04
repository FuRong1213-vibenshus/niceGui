import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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


weather_data = make_weather_table()


def update_plot() -> None:
    plot.figure.data = ()

    if checkbox_rain.value:
        fig.add_trace(
            go.Bar(
                x=weather_data.day,
                y=weather_data.rain,
                name="rain",
                marker_color="royalblue",
                opacity=0.3,
            ),
            secondary_y=True,
        )
    if checkbox_temp.value:
        fig.add_trace(
            go.Scatter(
                x=weather_data.day,
                y=weather_data.temperature,
                name="temp",
                mode="lines+markers",
            ),
            secondary_y=False,
        )
    fig.update_xaxes(
        title_text="Day",
    )
    fig.update_yaxes(
        title_text="Temperature (°C)",
        secondary_y=False,
        color="red",
    )
    fig.update_yaxes(
        title_text="Rain (mm)",
        secondary_y=True,
        color="royalblue",
        rangemode="tozero",
    )

    plot.update()


ui.label("Weather App").classes("text-2xl font-bold")
ui.label("Version 1 - UI basis").classes("text-gray-500")

with ui.row():
    checkbox_temp = ui.checkbox("Temperature", on_change=update_plot)

    checkbox_rain = ui.checkbox("Rain", on_change=update_plot)

fig = make_subplots(specs=[[{"secondary_y": True}]])
plot = ui.plotly(fig).classes("w-full")

ui.run()
