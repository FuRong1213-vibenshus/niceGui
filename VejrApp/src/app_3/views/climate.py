from nicegui import ui
import plotly.express as px
from app_3.models.models import CLIMATE_YEARS
from app_3.views.climate_viewmodel import ClimateViewModel


def climate_view() -> None:

    vm = ClimateViewModel()
    ui.label("Weather App - Version 3 - Climate").classes("text-2xl font-bold")

    with ui.card().classes("w-full"):
        ui.label("Choose the period")
        year_range = ui.range(
            min=CLIMATE_YEARS["min"],
            max=CLIMATE_YEARS["max"],
            value=vm.state.year_range,
        ).props(
            'label-always snap label-color="secondary"',
        )
        year_range.bind_value_to(vm.state, "year_range")
        # All years are already in state, so a new period only needs a new figure
        year_range.on_value_change(lambda: climate_figure.refresh())

    @ui.refreshable
    def climate_figure() -> None:
        if vm.state.error_message:
            ui.label(vm.state.error_message).classes("text-red-600")
            return

        climate_df = vm.state.daily_climate
        if climate_df.empty:
            ui.label("No climate data to show.")
            return

        years = climate_df["date"].dt.year
        start_year = vm.state.year_range["min"]
        end_year = vm.state.year_range["max"]
        climate_df = climate_df[(years >= start_year) & (years <= end_year)]

        yearly_df = (
            climate_df.groupby(climate_df["date"].dt.year)["temperature_2m_mean"]
            .mean()
            .rename_axis("year")
            .reset_index()
        )

        fig = px.line(
            yearly_df,
            x="year",
            y="temperature_2m_mean",
            markers=True,
            labels={"year": "Year", "temperature_2m_mean": "Mean temperature (°C)"},
        )
        ui.plotly(fig).classes("w-full h-96")

    vm.load_climate()
    climate_figure()
