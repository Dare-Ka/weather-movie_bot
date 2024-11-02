import asyncio

import aiohttp
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.main_menu.keyboard import main_menu_kb_builder
from bot.weather.keyboard import WeatherActionCb, WeatherAction
from bot.weather.state import Weather
from bot.weather.text import weather_error
from bot.weather.todays_weather.utils import get_weather_today
from .keyboard import (
    WeatherTodayCb,
    weather_today_kb_builder,
    weather_today_result_kb_builder,
)

router = Router(name=__name__)


@router.callback_query(
    WeatherActionCb.filter(F.action == WeatherAction.weather_today),
    flags={"chat_action": "typing"},
)
async def ask_city(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await asyncio.sleep(0.2)
    await callback.message.edit_text(
        "Выбери город из предложенных или введи нужный",
        reply_markup=weather_today_kb_builder(),
    )
    await state.set_state(Weather.weather_today)


@router.callback_query(WeatherTodayCb.filter(), flags={"chat_action": "typing"})
async def weather_today_with_cb(
    callback: CallbackQuery, callback_data: WeatherTodayCb, state: FSMContext
) -> None:
    await callback.answer()
    async with aiohttp.ClientSession() as http_session:
        weather = await get_weather_today(http_session, callback_data.city.value)
    if weather:
        await asyncio.sleep(0.2)
        await callback.message.edit_text(
            text=weather,
            reply_markup=weather_today_result_kb_builder(as_edit=False),
            parse_mode="HTML",
        )
    else:
        await asyncio.sleep(0.2)
        await callback.message.edit_text(
            text=weather_error, reply_markup=main_menu_kb_builder()
        )
    await state.clear()


@router.message(Weather.weather_today, flags={"chat_action": "typing"})
async def weather_today_with_fsm(message: Message, state: FSMContext) -> None:
    await state.update_data(city=message.text)
    context_data = await state.get_data()
    city = context_data.get("city")
    async with aiohttp.ClientSession() as http_session:
        weather = await get_weather_today(http_session, city)
    if weather:
        await asyncio.sleep(0.2)
        await message.answer(
            weather,
            parse_mode="HTML",
            reply_markup=weather_today_result_kb_builder(as_edit=False),
        )
    else:
        await asyncio.sleep(0.2)
        await message.reply(weather_error, reply_markup=main_menu_kb_builder())
    await state.clear()
