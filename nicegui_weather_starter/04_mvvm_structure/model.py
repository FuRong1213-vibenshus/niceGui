from dataclasses import dataclass


@dataclass
class WeatherPoint:
    time: str
    value: float


@dataclass
class WeatherQuery:
    station_id: str
    parameter_id: str
    start_time: str
    end_time: str

