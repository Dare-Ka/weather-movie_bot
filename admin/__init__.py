__all__ = ("router",)

from aiogram import Router

from .handler import router as admin_router

router = Router(name=__name__)

router.include_routers(
    admin_router,
)
