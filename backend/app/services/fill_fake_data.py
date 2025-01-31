import math
import random
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.weather import WeatherData


async def fill_mock_weather_data(
    session: AsyncSession,
    start_date: datetime,
    days: int = 30
):
    """
    Генерация фейковых (приближённых) погодных данных,
    по 1 записи на каждый час, в течение 'days' дней, начиная со start_date.

    :param session: асинхронная сессия SQLAlchemy
    :param start_date: начальное время (datetime)
    :param days: количество дней, за которые генерируются данные
    """
    total_hours = days * 24
    records_to_add = []

    for hour_offset in range(total_hours):
        current_time = start_date + timedelta(hours=hour_offset)

        # Пример "суточной" синусоиды для температуры: колебания от ~10 до ~25 градусов
        # Период синусоиды: 24 часа -> 2π * (hour_of_day / 24)
        hour_of_day = current_time.hour
        base_temp = 18  # "средняя" температура
        amplitude = 7  # размах колебаний (±7 градусов)
        temperature = base_temp + amplitude * math.sin(2 * math.pi * hour_of_day / 24)

        # Влажность в процентах: 40-80%, небольшие случайные колебания
        humidity = random.uniform(40, 80)

        # Давление: примерно 1010-1020 гПа
        pressure = 1015 + random.uniform(-5, 5)

        # Скорость ветра: 0-5 м/с
        wind_speed = random.uniform(0, 5)

        # Направление ветра: фиксированный список вариантов
        wind_direction = random.choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW"])

        # Тип осадков: пусть иногда идёт дождь
        precipitation_type = random.choice(["none", "snow", "none", "none"])

        # Интенсивность осадков: если дождь, от 0.1 до 2.0, иначе 0
        precipitation_intensity = 0.0
        if precipitation_type == "snow":
            precipitation_intensity = round(random.uniform(0.1, 2.0), 2)

        record = WeatherData(
            temperature=round(temperature, 2),
            humidity=round(humidity, 2),
            pressure=round(pressure, 2),
            wind_speed=round(wind_speed, 2),
            wind_direction=wind_direction,
            precipitation_type=precipitation_type,
            precipitation_intensity=precipitation_intensity,
            timestamp=current_time,
        )
        records_to_add.append(record)

    session.add_all(records_to_add)
    await session.commit()
    print(f"Успешно добавлено {len(records_to_add)} записей в weather_data.")
