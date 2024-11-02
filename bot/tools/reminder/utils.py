from aiogram import Bot

from bot.main_menu.keyboard import main_menu_kb_builder


async def reminder(bot: Bot, name, tg_id, event):
    await bot.send_message(
        chat_id=tg_id,
        text=f"{name}, напоминаю тебе:\n\n" + event,
        reply_markup=main_menu_kb_builder(),
    )
