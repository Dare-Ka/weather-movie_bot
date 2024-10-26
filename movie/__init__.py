__all__ = ("router",)

from aiogram import Router

from .find_movie_by_name.handler import router as movie_by_name_router
from .handler import router as movie_router
from .random_movie.handler import router as random_movie_router

router = Router(name=__name__)

router.include_routers(
    movie_router,
    random_movie_router,
    movie_by_name_router,
)
