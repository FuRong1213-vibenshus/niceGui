from dataclass import dataclass, field
from model import fetch_forecast
import pandas as pd


@dataclass
class WeatherState:
    city: str = "København"
    parameter: str = "temperature_2m"
    is_loading: bool = False
    error_message: str = ""
    forecast: pd.DataFrame = field(default_factory=pd.DataFrame)


class WeatherViewModel:
    def __init__(self) -> None:
        self.state = WeatherState()

        async def load_forecast(self) -> None:
            self.state.is_loading = True
            self.state.error_message = ""

            try:
                self.state.forecast = await fetch_forecast(
                    city=self.state.city,
                    parameter=self.state.parameter,
                )
            except Exception:
                self.state.error_message = "Vejrdata kunne ikke hentes."
