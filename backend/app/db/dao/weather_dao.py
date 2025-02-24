from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db_session
from app.db.models.weather import WeatherData, WeatherForecast


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
        existing_record = await self.session.execute(
            select(WeatherData).where(WeatherData.timestamp == timestamp))
        existing_record = existing_record.scalars().first()

        if existing_record:
            existing_record.temperature = temperature
            existing_record.humidity = humidity
            existing_record.pressure = pressure
            existing_record.wind_speed = wind_speed
            existing_record.wind_direction = wind_direction
            existing_record.precipitation_type = precipitation_type
            existing_record.precipitation_intensity = precipitation_intensity
        else:
            self.session.add(new_record)

        await self.session.commit()

    async def get_all_weather_data(self, limit: int, offset: int) -> List[WeatherData]:
        """
        Получить все записи погодных данных с пагинацией (limit/offset).
        """
        query = select(WeatherData).where(
            WeatherData.timestamp < datetime.now() + timedelta(hours=3)
        ).order_by(WeatherData.timestamp.desc()).limit(
            limit
        ).offset(offset)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())

    async def save_weather_forecast(
        self,
        forecast_time: datetime,
        timestamp: datetime,
        temperature: float,
        humidity: float,
        pressure: float,
        created_at: datetime
    ) -> None:
        """
        Сохранить прогноз в таблицу weather_forecast.
        """
        stmt = insert(WeatherForecast).values(
            forecast_time=forecast_time,
            timestamp=timestamp,
            temperature=temperature,
            humidity=humidity,
            pressure=pressure,
            created_at=created_at
        )
        await self.session.execute(stmt)

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

    async def get_latest_forecasts(self, limit: int = 24) -> List[WeatherForecast]:
        """
        Возвращает последние 'limit' прогнозов, отсортированные по времени прогноза
        (forecast_time) в убывающем порядке.
        """
        query = (
            select(WeatherForecast)
            .order_by(WeatherForecast.id.desc())
            .limit(limit)
        )
        rows = await self.session.execute(query)
        forecasts = rows.scalars().all()
        return list(forecasts)
