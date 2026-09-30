from nicegui import ui
import pandas as pd
import plotly.express as px
from app_3.views.forecast_viewmodel import ForecastViewModel
from app_3.models.models import STATIONS, PARAMETERS


def forecast_view() -> None:

    vm = ForecastViewModel()
    ui.label("Weather App - Version 3 - Page Routing ").classes("text-2xl font-bold")

    def update_forecast() -> None:
        vm.load_forecast()
        weather_figure_3day.refresh()
        weather_table_10day.refresh()

    with ui.card().classes("w-full"):
        ui.label("City Selection")
        station_selection = ui.select(
            options=list(STATIONS.keys()),
            value=vm.state.station,
            label="Station",
        )
        station_selection.bind_value_to(vm.state, "station")
        station_selection.on_value_change(update_forecast)

    @ui.refreshable
    def weather_figure_3day() -> None:
        if vm.state.error_message:
            ui.label(vm.state.error_message).classes("text-red-600")
            return
        df = vm.state.hourly_forecast
        start_date = df["date"].min().normalize()
        end_date = start_date + pd.Timedelta(days=3)

        three_day_df = df[(df["date"] >= start_date) & (df["date"] < end_date)]

        parameter_id = PARAMETERS[vm.state.parameter]

        fig = px.line(
            three_day_df,
            x="date",
            y=parameter_id,
            markers=True,
        )
        ui.plotly(fig).classes("w-full h-96")

    @ui.refreshable
    def weather_table_10day() -> None:
        if vm.state.error_message:
            ui.label(vm.state.error_message).classes("text-red-600")
            return

        daily_df = vm.state.daily_forecast.copy()

        daily_df["date"] = pd.to_datetime(daily_df["date"]).dt.strftime("%a %d/%m")
        daily_df = daily_df.rename(
            columns={
                "temperature_2m_min": "minimum",
                "temperature_2m_max": "maximum",
            }
        )
        daily_df["minimum"] = daily_df["minimum"].astype(float).round(1)
        daily_df["maximum"] = daily_df["maximum"].astype(float).round(1)
        columns = [
            {
                "name": "date",
                "label": "Day",
                "field": "date",
                "align": "left",
            },
            {
                "name": "minimum",
                "label": "Minimum (°C)",
                "field": "minimum",
                "align": "left",
            },
            {
                "name": "maximum",
                "label": "Maximum (°C)",
                "field": "maximum",
                "align": "left",
            },
        ]
        ui.table(
            columns=columns,
            rows=daily_df.to_dict("records"),
            row_key="date",
        ).classes("w-full")

    vm.load_forecast()
    weather_figure_3day()
    weather_table_10day()
