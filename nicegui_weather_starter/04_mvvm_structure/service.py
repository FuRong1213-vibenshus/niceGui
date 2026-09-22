import requests

from model import WeatherPoint, WeatherQuery


DMI_OBSERVATION_URL = "https://opendataapi.dmi.dk/v2/metObs/collections/observation/items"


class WeatherService:
    """Responsible for talking to the DMI API."""

    def get_observations(self, query: WeatherQuery) -> list[WeatherPoint]:
        params = {
            "stationId": query.station_id,
            "parameterId": query.parameter_id,
            "datetime": f"{query.start_time}/{query.end_time}",
            "limit": 100,
            "sortorder": "observed,ASC",
        }

        response = requests.get(DMI_OBSERVATION_URL, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()

        points = []
        for feature in data["features"]:
            props = feature["properties"]
            points.append(WeatherPoint(time=props["observed"], value=props["value"]))

        return points

