import datetime

from fastapi import APIRouter, Depends, HTTPException
from typing import Literal

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.db.dependencies import get_db_session
from app.services.fill_fake_data import fill_mock_weather_data
from app.services.forecast_service import ForecastService
from app.db.dao.weather_dao import WeatherDAO
from app.web.api.forecast.schema import WeatherForecastDTO

router = APIRouter()


@router.post("/run")
async def run_forecast(
    steps: int = 24,
    weather_dao: WeatherDAO = Depends(),
):
    """
    Запустить процесс генерации прогноза с помощью выбранной модели.
    """
    service = ForecastService(weather_dao)
    try:
        result = await service.generate_forecast(steps=steps)
        return {"detail": "Forecast created", "values": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/generate_fake_data")
async def generate_fake_data(
    session: AsyncSession = Depends(get_db_session),
):
    await fill_mock_weather_data(session, start_date=datetime.datetime(2025, 1, 1))


@router.get("/latest", response_model=list[WeatherForecastDTO])
async def get_latest_forecast(
    weather_dao: WeatherDAO = Depends(),
):
    """
    Получить последние N прогнозов из БД (пример).
    """
    latest_forecast = await weather_dao.get_latest_forecasts(limit=24)
    return latest_forecast
