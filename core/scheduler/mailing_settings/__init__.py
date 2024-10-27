__all__ = ("router",)

from aiogram import Router

from .handler import router as mailing_settings_router

router = Router(name=__name__)

router.include_router(
    mailing_settings_router,
)
