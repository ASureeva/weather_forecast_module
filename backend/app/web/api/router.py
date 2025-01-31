from fastapi.routing import APIRouter

from app.web.api import docs
from app.web.api.weather import views as weather_views
from app.web.api.forecast import views as forecast_views

api_router = APIRouter()
api_router.include_router(docs.router)
api_router.include_router(weather_views.router, prefix="/weather", tags=["weather"])
api_router.include_router(forecast_views.router, prefix="/forecast", tags=["forecast"])
