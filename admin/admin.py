from admin.admin_kb import iexit_kb
import config
from aiogram import Bot


async def error_handler(error: str, bot: Bot) -> None:
    """Notify the admin about errors with their description"""
    await bot.send_message(chat_id=config.ADMIN_ID, text=error, reply_markup=iexit_kb)


async def new_user_event(tg_id: int, tg_name: str, username: str, bot: Bot) -> None:
    """Notify the admin about new user"""
    await bot.send_message(chat_id=config.ADMIN_ID, text=f'Привет, у нас новый пользователь!\n'
                                                         f'Имя: {tg_name}\n'
                                                         f'ID: {tg_id}\n'
                                                         f'Username: {username}', reply_markup=iexit_kb)
