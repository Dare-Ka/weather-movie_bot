from admin.admin import new_user_event
from events.events_kb import donate_kb
from handlers.handlers_text import menu_text, hello, donate_text
from handlers.handlers_kb import imenu, menu_kb
from db.db import add_user_to_db, update_user
import asyncio
from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command('start'), flags={'chat_action': 'typing'})
async def start(message: Message, bot: Bot):
    await asyncio.sleep(0.2)
    await message.answer(hello.format(name=message.from_user.first_name), reply_markup=menu_kb)
    if message.from_user.username:
        await add_user_to_db(tg_id=message.from_user.id,
                             tg_name=message.from_user.first_name,
                             username='@' + message.from_user.username
                             )
        await new_user_event(tg_id=message.from_user.id,
                             tg_name=message.from_user.full_name,
                             username='@' + message.from_user.username,
                             bot=bot
                             )
    else:
        await add_user_to_db(tg_id=message.from_user.id,
                             tg_name=message.from_user.first_name,
                             username='Скрыто'
                             )
        await new_user_event(tg_id=message.from_user.id,
                             tg_name=message.from_user.full_name,
                             username='Скрыто',
                             bot=bot
                             )


@router.message(Command('donate'), flags={'chat_action': 'typing'})
async def donate(message: Message):
    await asyncio.sleep(0.2)
    await message.answer(donate_text, reply_markup=donate_kb)


@router.message(F.text == 'Меню')
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(message: Message):
    await message.answer(menu_text, reply_markup=imenu)
    if message.from_user.username:
        await update_user(tg_id=message.from_user.id,
                          tg_name=message.from_user.first_name,
                          username='@' + message.from_user.username
                          )
    else:
        await update_user(tg_id=message.from_user.id,
                          tg_name=message.from_user.first_name,
                          username='Скрыто'
                          )


@router.callback_query(F.data == 'menu')
async def menu(callback: types.CallbackQuery):
    await callback.message.answer(menu_text, reply_markup=imenu)
    if callback.from_user.username:
        await update_user(tg_id=callback.from_user.id,
                          tg_name=callback.from_user.first_name,
                          username='@' + callback.from_user.username
                          )
    else:
        await update_user(tg_id=callback.from_user.id,
                          tg_name=callback.from_user.first_name,
                          username='Скрыто'
                          )
