__all__ = ("router",)

from aiogram import Router

from admin import router as admin_router
from events import router as events_router
from meal.handler import router as meal_router
from movie import router as movie_router
from tools import router as tools_router
from weather import router as weather_router
from .handler import router as main_handler_router

router = Router(name=__name__)

router.include_routers(
    main_handler_router,
    tools_router,
    movie_router,
    weather_router,
    events_router,
    meal_router,
    admin_router,
)
