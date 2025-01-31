from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import DateTime, Float, Integer, String

from app.db.base import Base


class WeatherData(Base):
    """Модель для хранения данных, пришедших с датчиков."""

    __tablename__ = "weather_data"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    humidity: Mapped[float] = mapped_column(Float, nullable=False)
    pressure: Mapped[float] = mapped_column(Float, nullable=False)
    wind_speed: Mapped[float] = mapped_column(Float, nullable=True)
    wind_direction: Mapped[str] = mapped_column(String(50), nullable=True)
    precipitation_type: Mapped[str] = mapped_column(String(50), nullable=True)
    precipitation_intensity: Mapped[float] = mapped_column(Float, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
        default=datetime.utcnow,
    )


class WeatherForecast(Base):
    """Модель для хранения результатов прогноза погоды."""

    __tablename__ = "weather_forecast"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    forecast_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )
    temperature: Mapped[float] = mapped_column(Float, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )
    humidity: Mapped[float] = mapped_column(Float, nullable=True)
    pressure: Mapped[float] = mapped_column(Float, nullable=True)
    wind_speed: Mapped[float] = mapped_column(Float, nullable=True)
    wind_direction: Mapped[str] = mapped_column(String(50), nullable=True)
    precipitation_type: Mapped[str] = mapped_column(String(50), nullable=True)
    precipitation_intensity: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )
