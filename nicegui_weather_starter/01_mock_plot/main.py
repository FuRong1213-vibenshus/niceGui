from nicegui import ui
import pandas as pd
import plotly.express as px


def make_weather_table() -> pd.DataFrame:
    """Return fake weather data for the first app version."""
    return pd.DataFrame(
        {
            "day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "temperature": [12, 14, 13, 16, 15],
            "rain": [0.0, 1.5, 0.2, 0.0, 3.1],
        }
    )


def make_temperature_plot(df: pd.DataFrame):
    fig = px.line(
        df,
        x="day",
        y="temperature",
        markers=True,
        title="Temperature this week",
        labels={"day": "Day", "temperature": "Temperature, C"},
    )
    return fig


def make_precipitation_plot(df: pd.DataFrame):

    # TODO:: complete this function to return a bar plot (graph object) of precipitation

    pass


weather_data = make_weather_table()

ui.label("Weather App - Version 1 - UI basis").classes("text-2xl font-bold")

with ui.row():
    ui.button("Temperature")
    # TODO:
    # Add another button for rain
    #


# TODO:
# Modify this code, so that the plot for temperature or rain is displayed
# when the button is pressed.
#
ui.plotly(make_temperature_plot(weather_data)).classes("w-full")


ui.run()
