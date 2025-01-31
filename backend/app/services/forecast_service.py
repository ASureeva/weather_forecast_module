from datetime import datetime, timedelta

import pandas as pd

from app.db.dao.weather_dao import WeatherDAO
from app.forecasting.exp_smoothing import (
    train_exponential_smoothing,
    forecast_exponential_smoothing
)


class ForecastService:
    def __init__(self, weather_dao: WeatherDAO):
        self.weather_dao = weather_dao

    async def generate_forecast(
        self,
        steps: int = 24,
    ):
        """
        Забираем исторические данные (например, за последние 7 дней),
        тренируем 3 отдельные модели Exponential Smoothing по (temperature, humidity, pressure),
        делаем прогноз на 'steps' часов для каждого параметра.
        Сохраняем результат в БД (weather_forecast) — 1 запись на каждый час.
        """
        records = await self.weather_dao.get_all_weather_data(limit=99999, offset=0)
        if not records:
            raise ValueError("Нет данных для обучения модели.")

        # 2. Преобразуем список WeatherData -> pandas DataFrame
        df = self._to_dataframe(records)  # см. метод ниже

        # 3. Отдельно тренируем Exponential Smoothing для каждого признака
        fitted_temp = train_exponential_smoothing(
            df, col_name="temperature", seasonal_periods=24
        )
        fitted_hum = train_exponential_smoothing(
            df, col_name="humidity", seasonal_periods=24
        )
        fitted_pres = train_exponential_smoothing(
            df, col_name="pressure", seasonal_periods=24
        )

        # 4. Получаем прогнозы на 'steps' часов вперёд
        forecast_vals_temp = forecast_exponential_smoothing(fitted_temp, steps=steps)
        forecast_vals_hum = forecast_exponential_smoothing(fitted_hum, steps=steps)
        forecast_vals_pres = forecast_exponential_smoothing(fitted_pres, steps=steps)

        # 5. Сохраняем прогноз в таблицу weather_forecast (1 запись на каждый час)
        now = datetime.utcnow()
        for i in range(steps):
            forecast_time = now + timedelta(hours=i + 1)

            if forecast_time.minute < 30:
                timestamp = forecast_time.replace(minute=0, second=0,
                                                            microsecond=0)
            else:
                timestamp = (
                        forecast_time + timedelta(hours=1)).replace(
                    minute=0, second=0, microsecond=0)
            await self.weather_dao.save_weather_forecast(
                forecast_time=forecast_time,
                timestamp=timestamp,
                temperature=float(round(forecast_vals_temp[i], 1)),
                humidity=float(round(forecast_vals_hum[i], 1)),
                pressure=float(round(forecast_vals_pres[i], 1)),
                created_at=now,
            )

        return {
            "temperature": forecast_vals_temp.tolist(),
            "humidity": forecast_vals_hum.tolist(),
            "pressure": forecast_vals_pres.tolist(),
        }

    def _to_dataframe(self, records):
        """
        Преобразование списка WeatherData -> pd.DataFrame c DatetimeIndex.
        Предполагается, что у каждого WeatherData есть:
         - .timestamp,
         - .temperature,
         - .humidity,
         - .pressure
        """
        data = {
            "timestamp": [r.timestamp for r in records],
            "temperature": [r.temperature for r in records],
            "humidity": [r.humidity for r in records],
            "pressure": [r.pressure for r in records],
        }
        df = pd.DataFrame(data)
        df.sort_values(by="timestamp", inplace=True)
        df.set_index("timestamp", inplace=True)
        return df
