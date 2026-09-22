from nicegui import ui
import json
from pathlib import Path


FAVORITES_FILE = Path("favorites.json")


def load_favorites() -> list[dict]:
    if not FAVORITES_FILE.exists():
        return []

    with FAVORITES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_favorites(favorites: list[dict]) -> None:
    with FAVORITES_FILE.open("w", encoding="utf-8") as file:
        json.dump(favorites, file, indent=2)


favorites = load_favorites()


def add_favorite():
    favorite = {
        "name": name_input.value,
        "longitude": longitude_input.value,
        "latitude": latitude_input.value,
    }

    # TODO: Validate that name, longitude, and latitude are filled in.
    favorites.append(favorite)
    save_favorites(favorites)
    favorite_list.refresh()


@ui.refreshable
def favorite_list():
    if not favorites:
        ui.label("No favorites yet.")
        return

    for favorite in favorites:
        with ui.row().classes("items-center"):
            ui.label(favorite["name"]).classes("font-bold")
            ui.label(f'{favorite["longitude"]}, {favorite["latitude"]}')
            # TODO: Add a button that loads forecast for this favorite.
            # TODO: Add a button that removes this favorite.


ui.label("Weather App - Version 5").classes("text-2xl font-bold")
ui.label("This version starts an extension with saved favorite places.")

with ui.row().classes("items-end"):
    name_input = ui.input("Place name", value="Copenhagen")
    longitude_input = ui.input("Longitude", value="12.561")
    latitude_input = ui.input("Latitude", value="55.715")
    ui.button("Add favorite", on_click=add_favorite)

favorite_list()

# TODO: Combine this file with the forecast app from version 3.
# TODO: Add compare mode: choose two favorite places and plot them together.

ui.run()

