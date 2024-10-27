from aiogram import Bot

from core.config import settings
from core.models import User
from main_menu.keyboard import main_menu_kb_builder


async def error_notifier(func_name: str, error: str) -> None:
    bot = Bot(token=settings.TESTS_BOT_TOKEN)
    description = f"{func_name}:\n{error}"
    await bot.send_message(
        chat_id=settings.MAKSIM_ID,
        text=description,
        reply_markup=main_menu_kb_builder(),
    )


async def new_user_event(user: User) -> None:
    """Notify the admin about new user"""
    bot = Bot(token=settings.TESTS_BOT_TOKEN)
    await bot.send_message(
        chat_id=settings.ADMIN_ID,
        text=f"Привет, у нас новый пользователь!\n"
        f"Имя: {user.tg_name}\n"
        f"ID: {user.tg_id}\n"
        f"Username: {user.username}",
        reply_markup=main_menu_kb_builder(),
    )
