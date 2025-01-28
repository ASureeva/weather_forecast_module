from datetime import datetime
from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db_session
from app.db.models.weather import WeatherData


class WeatherDAO:
    """Класс для доступа к таблице weather_data."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        """
        Зависимость (Depends) обеспечивает передачу асинхронной сессии
        при создании объекта DAO в эндпоинте.
        """
        self.session = session

    async def create_weather_data(
        self,
        temperature: float,
        humidity: float,
        pressure: float,
        wind_speed: Optional[float],
        wind_direction: Optional[str],
        precipitation_type: Optional[str],
        precipitation_intensity: Optional[float],
        timestamp: datetime,
    ) -> None:
        """
        Создание новой записи в таблице weather_data.
        """
        new_record = WeatherData(
            temperature=temperature,
            humidity=humidity,
            pressure=pressure,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            precipitation_type=precipitation_type,
            precipitation_intensity=precipitation_intensity,
            timestamp=timestamp,
        )
        self.session.add(new_record)

    async def get_all_weather_data(self, limit: int, offset: int) -> List[WeatherData]:
        """
        Получить все записи погодных данных с пагинацией (limit/offset).
        """
        query = select(WeatherData).limit(limit).offset(offset)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())

    async def filter_weather_data(
        self,
        wind_direction: Optional[str] = None,
    ) -> List[WeatherData]:
        """
        Пример фильтрации по направлению ветра (или любому другому критерию).
        """
        query = select(WeatherData)
        if wind_direction:
            query = query.where(WeatherData.wind_direction == wind_direction)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())
