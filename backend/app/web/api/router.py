from fastapi.routing import APIRouter

from app.web.api import docs
from app.web.api.weather import views as weather_views

api_router = APIRouter()
api_router.include_router(docs.router)
api_router.include_router(weather_views.router, prefix="/weather", tags=["weather"])
