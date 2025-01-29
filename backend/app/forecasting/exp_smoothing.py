import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing


def train_exponential_smoothing(
    df: pd.DataFrame,
    col_name: str = "temperature",
    trend: str = "add",
    seasonal: str = "add",
    seasonal_periods: int = 24
):
    """
    Обучение модели экспоненциального сглаживания (Holt-Winters).
    :param trend: "add" или "mul"
    :param seasonal: "add" или "mul"
    :param seasonal_periods: период сезонности (для часов - 24, для дней - 7, ...)
    """
    series = df[col_name]
    model = ExponentialSmoothing(
        series,
        trend=trend,
        seasonal=seasonal,
        seasonal_periods=seasonal_periods,
    )
    fitted = model.fit()
    return fitted


def forecast_exponential_smoothing(
    fitted_model,
    steps: int = 24
) -> np.ndarray:
    """
    Прогноз на steps шагов вперёд.
    """
    forecast_result = fitted_model.forecast(steps=steps)
    return forecast_result.values
