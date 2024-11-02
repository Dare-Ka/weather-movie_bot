__all__ = ("router",)

from aiogram import Router

from .handler import router as tools_router
from .reminder.handler import router as reminder_router
from .todo_list.handler import router as todo_list_router

router = Router(name=__name__)

router.include_routers(
    tools_router,
    reminder_router,
    todo_list_router,
)
