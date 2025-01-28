import datetime
from typing import List

from fastapi import APIRouter, Depends

from app.db.dao.weather_dao import WeatherDAO
from app.db.models.weather import WeatherData
from app.web.api.weather.schema import WeatherDataDTO, WeatherDataInputDTO

router = APIRouter()


@router.get("/", response_model=List[WeatherDataDTO])
async def get_weather_data(
    limit: int = 10,
    offset: int = 0,
    weather_dao: WeatherDAO = Depends(),
) -> List[WeatherData]:
    """
    Получить все записи о погоде из БД.
    """
    return await weather_dao.get_all_weather_data(limit=limit, offset=offset)


@router.post("/")
async def create_weather_data(
    new_weather: WeatherDataInputDTO,
    weather_dao: WeatherDAO = Depends(),
) -> None:
    """
    Создать новую запись о погоде в БД.
    """
    timestamp_utc_naive = new_weather.timestamp.astimezone(
        datetime.timezone.utc,
    ).replace(tzinfo=None)
    await weather_dao.create_weather_data(
        temperature=new_weather.temperature,
        humidity=new_weather.humidity,
        pressure=new_weather.pressure,
        wind_speed=new_weather.wind_speed,
        wind_direction=new_weather.wind_direction,
        precipitation_type=new_weather.precipitation_type,
        precipitation_intensity=new_weather.precipitation_intensity,
        timestamp=timestamp_utc_naive,
    )
