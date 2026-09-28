from dataclasses import dataclass, field
from model import fetch_forecast
import pandas as pd


@dataclass
class WeatherState:
    city: str = "Copenhagen"
    parameter: str = "temperature_2m"
    forecast_days: int = 3
    is_loading: bool = False
    error_message: str = ""
    temp_forecast: pd.DataFrame = field(default_factory=pd.DataFrame)
    rain_3day: pd.DataFrame = field(default_factory=pd.DataFrame)


class WeatherViewModel:
    def __init__(self) -> None:
        self.state = WeatherState()

    def load_temp_forecast(self) -> None:
        self.state.is_loading = True
        self.state.error_message = ""

        try:
            self.state.temp_forecast = fetch_forecast(
                address=self.state.city,
                parameter=self.state.parameter,
                forecast_days=self.state.forecast_days,
            )
        except Exception:
            self.state.error_message = "Vejrdata kunne ikke hentes."
