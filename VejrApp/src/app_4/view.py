from nicegui import ui
import plotly.express as px
from viewmodel import AirQualityViewModel


def airquality_view():

    vm = AirQualityViewModel()

    def update_forecast():
        vm.load_forecast()
        airquality_figure.refresh()

    ui.label("Airquality App").classes("text-2xl font-bold")
    with ui.card().classes("w-full"):
        ui.label("City selection")
        station_selection = ui.select(
            options=["Copenhagen", "Odense", "Arhus"],
            value=vm.state.station,
            label="Station",
        )
        station_selection.bind_value_to(vm.state, "station")
        station_selection.on_value_change(update_forecast)

    @ui.refreshable
    def airquality_figure():

        fig = px.line(
            vm.state.airqualityforecast,
            x="date",
            y="pm2_5",
        )
        ui.plotly(fig).classes("w-full h-96")

    vm.load_forecast()
    airquality_figure()


airquality_view()
ui.run()
