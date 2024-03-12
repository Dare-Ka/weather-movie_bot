from admin.admin import error_handler
from settings.states import Scheduler
from events.events import reminder
from events.events_kb import times_kb, reminder_back
from events.events_text import send_message
from db.db import update_user
import asyncio
from random import choice
from aiogram import types, F, Bot, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler


router = Router()


@router.callback_query(F.data == 'create_event', flags={'chat_action': 'typing'})
async def ask_date(callback: types.CallbackQuery, state: FSMContext):
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
    await asyncio.sleep(0.2)
    await callback.message.answer('Привет! Через сколько часов напомнить?')
    await callback.message.answer_sticker(sticker=choice(send_message),
                                          reply_markup=times_kb
                                          )
    await state.set_state(Scheduler.date)


@router.message(Scheduler.date, flags={'chat_action': 'typing'})
async def ask_event(message: Message, state: FSMContext, bot: Bot):
    try:
        await state.update_data(delta=float(message.text))
        await asyncio.sleep(0.2)
        await message.answer('Что напомнить?')
        await message.answer_sticker(sticker=choice(send_message))
        await state.set_state(Scheduler.event)
    except Exception as error:
        await message.answer('Произошла ошибка..😔\n'
                             'Попроуем еще раз?',
                             parse_mode="HTML",
                             reply_markup=reminder_back
                             )
        await error_handler('ask_event:\n' + str(error), bot)
        await state.clear()


@router.message(Scheduler.event, flags={'chat_action': 'typing'})
async def add_event(message: Message, state: FSMContext, apscheduler: AsyncIOScheduler):
    await state.update_data(event=message.text)
    context_data = await state.get_data()
    delta = context_data.get('delta')
    event = context_data.get('event')
    tg_id = message.from_user.id
    name = message.from_user.first_name
    await asyncio.sleep(0.2)
    await message.answer(f'Запомнил!👍', reply_markup=reminder_back)
    await state.clear()
    apscheduler.add_job(reminder,
                        trigger='date',
                        run_date=datetime.now() + timedelta(hours=delta),
                        kwargs={'name': name, 'tg_id': tg_id, 'event': event}
                        )
