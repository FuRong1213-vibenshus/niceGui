from nicegui import ui
import plotly.express as px
from options import STATIONS
from viewmodel_clean import WeatherViewModel

DAILY_COLUMNS = [
    {"name": "date", "label": "Day", "field": "date", "align": "left"},
    {"name": "minimum", "label": "Minimum (°C)", "field": "minimum", "align": "left"},
    {"name": "maximum", "label": "Maximum (°C)", "field": "maximum", "align": "left"},
]


def weather_view() -> None:

    vm = WeatherViewModel()
    ui.label("Weather App - Version 2 - MVVM architecture ").classes(
        "text-2xl font-bold"
    )

    def update_forecast() -> None:
        vm.load_forecast()
        weather_figure_3day.refresh()
        precipitation_figure_3day.refresh()
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
        fig = px.line(
            vm.state.three_day_forecast,
            x="date",
            y=vm.state.parameter_id,
            markers=True,
        )
        ui.plotly(fig).classes("w-full h-96")

    @ui.refreshable
    def precipitation_figure_3day() -> None:
        if vm.state.error_message:
            return
        fig = px.bar(
            vm.state.three_day_forecast,
            x="date",
            y="precipitation",
            labels={"precipitation": "precipitation (mm)"},
        )
        ui.plotly(fig).classes("w-full h-96")

    @ui.refreshable
    def weather_table_10day() -> None:
        if vm.state.error_message:
            ui.label(vm.state.error_message).classes("text-red-600")
            return
        ui.table(
            columns=DAILY_COLUMNS,
            rows=vm.state.daily_rows,
            row_key="date",
        ).classes("w-full")

    vm.load_forecast()
    weather_figure_3day()
    precipitation_figure_3day()
    weather_table_10day()


weather_view()
ui.run()
