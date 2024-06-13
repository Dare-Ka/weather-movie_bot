from admin.admin import new_user_event
from events.events_kb import donate_kb
from handlers.handlers_text import menu_text, hello, donate_text
from handlers.handlers_kb import imenu
from db.models import db, backup_db
import asyncio
from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command('start'), flags={'chat_action': 'typing'})
async def start(message: Message, bot: Bot):
    await asyncio.sleep(0.2)
    await message.answer(hello.format(name=message.from_user.first_name), reply_markup=imenu)
    await db.add_user_to_db(
        tg_id=message.from_user.id,
        tg_name=message.from_user.first_name,
        username=message.from_user.username
                            )
    await backup_db.add_user_to_db(
        tg_id=message.from_user.id,
        tg_name=message.from_user.first_name,
        username=message.from_user.username
    )
    await new_user_event(tg_id=message.from_user.id,
                         tg_name=message.from_user.full_name,
                         username='@' + message.from_user.username,
                         bot=bot
                         )


@router.message(Command('donate'), flags={'chat_action': 'typing'})
async def donate(message: Message):
    await asyncio.sleep(0.2)
    await message.answer(donate_text, reply_markup=donate_kb)


@router.message(F.text.lower() == 'меню')
@router.message(F.text.lower() == "выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(message: Message):
    await message.answer(menu_text, reply_markup=imenu)


@router.callback_query(F.data == 'menu')
async def menu(callback: types.CallbackQuery):
    await callback.message.answer(menu_text, reply_markup=imenu)
