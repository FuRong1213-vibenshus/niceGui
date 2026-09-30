from nicegui import ui
from app_3.views.forecast import forecast_view
from app_3.views.history import history_view


def root():
    with ui.header():
        ui.label("Weather app")
    with ui.left_drawer():
        ui.link("Forecast", "/")
        ui.link("Historic data", "/history")

    ui.sub_pages({"/": forecast_view, "/history": history_view})


ui.run(root, reload=False)
