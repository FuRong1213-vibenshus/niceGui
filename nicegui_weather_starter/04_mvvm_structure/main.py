from nicegui import ui

from viewmodel import WeatherViewModel


vm = WeatherViewModel()


def sync_inputs_to_viewmodel():
    vm.station_id = station_input.value
    vm.parameter_id = parameter_select.value


def load_weather():
    sync_inputs_to_viewmodel()
    vm.load()
    chart.figure = vm.make_figure()
    chart.update()

    # TODO: Show vm.error_message if something went wrong.


ui.label("Weather App - Version 4").classes("text-2xl font-bold")
ui.label("This version separates model, service, viewmodel, and view.")

with ui.row().classes("items-end"):
    station_input = ui.input("Station ID", value=vm.station_id)
    parameter_select = ui.select(
        ["temp_dry", "humidity", "wind_speed"],
        value=vm.parameter_id,
        label="Parameter",
    )
    ui.button("Load", on_click=load_weather)

chart = ui.plotly(vm.make_figure()).classes("w-full")

# TODO: Add a row with min, max, and average values.

ui.run()

