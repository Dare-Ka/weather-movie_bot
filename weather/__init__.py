__all__ = ("router",)

from aiogram import Router

from .handler import router as common_weather_router
from .three_days_weather.handler import router as three_days_weather_router
from .todays_weather.handler import router as one_day_weather_router

router = Router(name=__name__)

router.include_routers(
    common_weather_router,
    one_day_weather_router,
    three_days_weather_router,
)
