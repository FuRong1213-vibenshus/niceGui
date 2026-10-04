from nicegui import ui
from app_3.views.forecast import forecast_view
from app_3.views.climate import climate_view


def root():
    with ui.header():
        ui.label("Weather app")
    with ui.left_drawer():
        ui.link("Forecast", "/")
        ui.link("Climate", "/climate")
    ui.query(".nicegui-content").classes("w-full")
    ui.sub_pages({"/": forecast_view, "/climate": climate_view}).classes("w-full")


if __name__ == "__main__":
    ui.run(root, reload=False)
