__all__ = ("router",)

from aiogram import Router

from bot.admin import router as admin_router
from bot.core.scheduler.mailing_settings import router as scheduler_router
from bot.events import router as events_router
from bot.meal.handler import router as meal_router
from bot.movie import router as movie_router
from bot.tools import router as tools_router
from bot.weather import router as weather_router
from .handler import router as main_handler_router

router = Router(name=__name__)

router.include_routers(
    main_handler_router,
    tools_router,
    movie_router,
    weather_router,
    meal_router,
    scheduler_router,
    admin_router,
    events_router,
)
