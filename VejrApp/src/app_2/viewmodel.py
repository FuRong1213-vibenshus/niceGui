from dataclasses import dataclass, field
from options import PARAMETERS
from model import fetch_forecast
import pandas as pd


@dataclass
class WeatherState:
    station: str = "Copenhagen"
    parameter: str = "temperature"
    forecast_days: int = 10
    is_loading: bool = False
    error_message: str = ""
    hourly_forecast: pd.DataFrame = field(default_factory=pd.DataFrame)
    daily_forecast: pd.DataFrame = field(default_factory=pd.DataFrame)


class WeatherViewModel:
    def __init__(self) -> None:
        self.state = WeatherState()

    def change_station(self, city: str):
        self.state.station = city
        self.load_forecast()

    def change_parameter(self, parameter: str):
        self.state.parameter = parameter
        self.load_forecast()

    def load_forecast(self) -> None:
        self.state.is_loading = True
        self.state.error_message = ""

        try:
            parameter_id = PARAMETERS[self.state.parameter]
            hourly, daily = fetch_forecast(
                address=self.state.station,
                parameter=parameter_id,
                forecast_days=self.state.forecast_days,
            )
            self.state.hourly_forecast = hourly
            self.state.daily_forecast = daily
        except Exception as error:
            print(repr(error))
            self.state.error_message = "Vejrdata kunne ikke hentes."
        finally:
            self.state.is_loading = False
