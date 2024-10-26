import asyncio
from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from main_menu.keyboard import main_menu_kb_builder
from tools.keyboard import ToolsActionsCb, ToolsActions
from .keyboard import (
    hours_kb,
    ReminderCallbackData,
    minutes_kb,
)
from .state import Reminder
from .utils import reminder

router = Router(name=__name__)


@router.callback_query(
    ToolsActionsCb.filter(F.action == ToolsActions.create_event),
    flags={"chat_action": "typing"},
)
async def ask_date(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.answer()
    await callback.message.edit_text(
        "Привет!\nЧерез сколько часов напомнить?",
        reply_markup=hours_kb(),
    )
    await state.set_state(Reminder.hour)


@router.message(Reminder.hour, flags={"chat_action": "typing"})
async def set_time_with_text(message: Message, state: FSMContext) -> None:
    await state.update_data(delta_hour=float(message.text))
    await message.answer("Через сколько минут напомнить?", reply_markup=minutes_kb())
    await state.set_state(Reminder.minute)


@router.message(Reminder.minute, flags={"chat_action": "typing"})
async def set_minute_with_text(message: Message, state: FSMContext) -> None:
    await state.update_data(delta_minute=float(message.text))
    await message.answer("Что напомнить?")
    await state.set_state(Reminder.event)


@router.callback_query(
    ReminderCallbackData.filter(F.hour), flags={"chat_action": "typing"}
)
async def set_hour_with_kb(
    callback: CallbackQuery, callback_data: ReminderCallbackData, state: FSMContext
) -> None:
    await state.clear()
    await callback.answer()
    await state.update_data(delta_hour=float(callback_data.hour.value))
    await callback.message.edit_text(
        "Через сколько минут напомнить?",
        reply_markup=minutes_kb(),
    )
    await state.set_state(Reminder.minute)


@router.callback_query(
    ReminderCallbackData.filter(F.minute), flags={"chat_action": "typing"}
)
async def set_minute_with_kb(
    callback: CallbackQuery,
    callback_data: ReminderCallbackData,
    state: FSMContext,
) -> None:
    await callback.answer()
    await state.update_data(delta_minute=float(callback_data.minute.value))
    await callback.message.edit_text("Что напомнить?")
    await state.set_state(Reminder.event)


@router.message(Reminder.event, flags={"chat_action": "typing"})
async def add_event(
    message: Message, state: FSMContext, apscheduler: AsyncIOScheduler
) -> None:
    await state.update_data(event=message.text)
    context_data = await state.get_data()
    delta_hour = context_data.get("delta_hour")
    delta_minute = context_data.get("delta_minute")
    event = context_data.get("event")
    tg_id = message.from_user.id
    name = message.from_user.first_name
    await asyncio.sleep(0.2)
    apscheduler.add_job(
        reminder,
        trigger="date",
        run_date=datetime.now() + timedelta(hours=delta_hour, minutes=delta_minute),
        kwargs={"name": name, "tg_id": tg_id, "event": event},
    )
    await message.answer(f"Запомнил!👍", reply_markup=main_menu_kb_builder())
    await state.clear()
