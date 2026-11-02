from dataclasses import dataclass, field
import pandas as pd
from model import fetch_forecast


@dataclass
class AirQualityState:
    station: str = "Copenhagen"
    airqualityforecast: pd.DataFrame = field(default_factory=pd.DataFrame)


class AirQualityViewModel:
    def __init__(self):
        self.state = AirQualityState()

    def load_forecast(self):
        self.state.airqualityforecast = fetch_forecast(
            address=self.state.station,
            parameter="pm2_5",
        )
