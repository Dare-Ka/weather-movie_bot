__all__ = ("router",)

from aiogram import Router

from .reactions.handler import router as reactions_router

router = Router(name=__name__)

router.include_routers(
    reactions_router,
)
