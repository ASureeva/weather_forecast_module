import datetime
from typing import List

from fastapi import APIRouter, Depends

from app.db.dao.weather_dao import WeatherDAO
from app.db.models.weather import WeatherData
from app.web.api.weather.schema import WeatherDataDTO, WeatherDataInputDTO
from app.services.current_weather import get_current_weather

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

    MOSCOW_TZ = datetime.timezone(datetime.timedelta(hours=0))

    timestamp_moscow = new_weather.timestamp.astimezone(MOSCOW_TZ)

    if timestamp_moscow.minute < 30:
        timestamp_moscow = timestamp_moscow.replace(minute=0, second=0, microsecond=0)
    else:
        timestamp_moscow = (timestamp_moscow + datetime.timedelta(hours=1)).replace(
            minute=0, second=0, microsecond=0)

    timestamp_moscow_naive = timestamp_moscow.replace(tzinfo=None)

    result = await get_current_weather()

    await weather_dao.create_weather_data(
        temperature=new_weather.temperature,
        humidity=new_weather.humidity,
        pressure=new_weather.pressure,
        wind_speed=result['wind_speed'],
        wind_direction=result['wind_direction'],
        precipitation_type=result['precipitation_type'],
        precipitation_intensity=result['precipitation_intensity'],
        timestamp=timestamp_moscow_naive,
    )
