from dataclasses import dataclass
import pandas as pd


@dataclass
class WeatherQuery:
    station_id: str
    parameter_id: str
    start_time: str
    end_time: str
    forecast: pd.DataFrame


place2Coordinate = {
    "Copenhagen": (55.676, 12.568),
    "Arhus": (56.158150, 10.212030),
    "Odense": (55.396229, 10.390600),
}
