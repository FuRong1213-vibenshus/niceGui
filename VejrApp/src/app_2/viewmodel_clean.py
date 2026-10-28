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
    # Display-ready data, so the view only has to draw it.
    parameter_id: str = "temperature_2m"
    three_day_forecast: pd.DataFrame = field(default_factory=pd.DataFrame)
    daily_rows: list[dict] = field(default_factory=list)


def first_three_days(df: pd.DataFrame) -> pd.DataFrame:
    start_date = df["date"].min().normalize()
    end_date = start_date + pd.Timedelta(days=3)
    return df[(df["date"] >= start_date) & (df["date"] < end_date)]


def daily_table_rows(daily: pd.DataFrame) -> list[dict]:
    return [
        {
            "date": row.date.strftime("%a %d/%m"),
            "minimum": round(float(row.temperature_2m_min), 1),
            "maximum": round(float(row.temperature_2m_max), 1),
        }
        for row in daily.itertuples()
    ]


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
            self.state.parameter_id = PARAMETERS[self.state.parameter]
            hourly, daily = fetch_forecast(
                address=self.state.station,
                parameter=self.state.parameter_id,
                forecast_days=self.state.forecast_days,
            )
            self.state.hourly_forecast = hourly
            self.state.daily_forecast = daily
            self.state.three_day_forecast = first_three_days(hourly)
            self.state.daily_rows = daily_table_rows(daily)
        except Exception as error:
            print(repr(error))
            self.state.error_message = "Vejrdata kunne ikke hentes."
        finally:
            self.state.is_loading = False
