from aiogram import Bot

from core.config import settings
from main_menu.keyboard import main_menu_kb_builder


async def error_notifier(func_name: str, error: str) -> None:
    bot = Bot(token=settings.TESTS_BOT_TOKEN)
    description = f"{func_name}:\n{error}"
    await bot.send_message(
        chat_id=settings.MAKSIM_ID,
        text=description,
        reply_markup=main_menu_kb_builder(),
    )
