import pandas as pd
import plotly.express as px

from model import WeatherQuery
from service import WeatherService


class WeatherViewModel:
    """Stores app state and prepares data for the UI."""

    def __init__(self):
        self.station_id = "06149"
        self.parameter_id = "temp_dry"
        self.start_time = "2018-02-12T00:00:00Z"
        self.end_time = "2018-02-13T00:00:00Z"
        self.points = []
        self.error_message = ""
        self.service = WeatherService()

    def load(self):
        query = WeatherQuery(
            station_id=self.station_id,
            parameter_id=self.parameter_id,
            start_time=self.start_time,
            end_time=self.end_time,
        )

        # TODO: Add try/except and save a helpful error message.
        self.points = self.service.get_observations(query)

    def as_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(
            [{"time": point.time, "value": point.value} for point in self.points]
        )

    def make_figure(self):
        df = self.as_dataframe()
        return px.line(
            df,
            x="time",
            y="value",
            title=f"{self.parameter_id} from station {self.station_id}",
        )

    # TODO: Add a method that calculates min, max, and average.

