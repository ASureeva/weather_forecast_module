from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class WeatherForecastDTO(BaseModel):
    """
    DTO (Data Transfer Object) для сериализации прогноза.
    """
    id: int
    forecast_time: datetime
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_direction: Optional[str] = None
    precipitation_type: Optional[str] = None
    precipitation_intensity: Optional[float] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
