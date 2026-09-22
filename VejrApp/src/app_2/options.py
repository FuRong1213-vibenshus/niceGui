"""Small DMI choices used by the app.

Students can add more stations and parameters here without changing main.py.
"""

DMI_OBSERVATION_URL = "https://opendataapi.dmi.dk/v2/metObs/collections/observation/items"

DATE_RANGE = "2018-02-12T00:00:00Z/2018-02-13T00:00:00Z"

STATIONS = {
    "Copenhagen / Koebenhavn": "06149",
    # TODO: Add more DMI station names and station IDs.
}

PARAMETERS = {
    "Temperature": "temp_dry",
    "Humidity": "humidity",
    "Wind speed": "wind_speed",
    # TODO: Add more parameters from DMI Frie Data.
}

