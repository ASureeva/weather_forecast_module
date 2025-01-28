from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class WeatherDataDTO(BaseModel):
    """
    DTO (Data Transfer Object) для возврата данных о погоде из БД.
    """

    id: int
    temperature: float
    humidity: float
    pressure: float
    wind_speed: Optional[float] = None
    wind_direction: Optional[str] = None
    precipitation_type: Optional[str] = None
    precipitation_intensity: Optional[float] = None
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class WeatherDataInputDTO(BaseModel):
    """
    DTO для создания новой записи о погоде.
    """

    temperature: float
    humidity: float
    pressure: float
    wind_speed: Optional[float] = None
    wind_direction: Optional[str] = None
    precipitation_type: Optional[str] = None
    precipitation_intensity: Optional[float] = None
    timestamp: datetime
