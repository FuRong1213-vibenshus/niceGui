from dataclasses import dataclass, field
import pandas as pd
from app_3.models.models import CLIMATE_YEARS
from app_3.models.services import fetch_climate


@dataclass
class ClimateState:
    station: str = "Copenhagen"
    parameter: str = "temperature"
    year_range: dict = field(default_factory=lambda: dict(CLIMATE_YEARS))
    is_loading: bool = False
    error_message: str = ""
    daily_climate: pd.DataFrame = field(default_factory=pd.DataFrame)


class ClimateViewModel:
    def __init__(self) -> None:
        self.state = ClimateState()

    def load_climate(self) -> None:
        self.state.is_loading = True
        self.state.error_message = ""

        try:
            # Fetch the whole period once. The view shows the years chosen in state.year_range.
            self.state.daily_climate = fetch_climate(year_range=CLIMATE_YEARS)
        except Exception as error:
            print(repr(error))
            self.state.daily_climate = pd.DataFrame()
            self.state.error_message = "Klimadata kunne ikke hentes."
        finally:
            self.state.is_loading = False
