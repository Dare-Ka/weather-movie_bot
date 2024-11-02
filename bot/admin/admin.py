from aiogram import Bot

from bot.core.config import settings
from bot.core.models import User
from bot.main_menu.keyboard import main_menu_kb_builder


async def error_notifier(func_name: str, error: str) -> None:
    """Notify the admin about errors"""
    bot = Bot(token=settings.bot.token)
    description = f"{func_name}:\n{error}"
    await bot.send_message(
        chat_id=settings.bot.admin_id,
        text=description,
        reply_markup=main_menu_kb_builder(),
    )


async def new_user_event(user: User) -> None:
    """Notify the admin about new user"""
    bot = Bot(token=settings.bot.token)
    await bot.send_message(
        chat_id=settings.bot.admin_id,
        text=f"Привет, у нас новый пользователь!\n"
        f"Имя: {user.tg_name}\n"
        f"ID: {user.tg_id}\n"
        f"Username: @{user.username}",
        reply_markup=main_menu_kb_builder(),
    )
