import asyncio

import aiohttp
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from main_menu.keyboard import main_menu_kb_builder
from weather.keyboard import WeatherActionCb, WeatherAction
from weather.state import Weather
from weather.text import weather_error
from weather.three_days_weather.keyboard import (
    WeatherThreeDaysCb,
    weather_three_days_kb_builder,
    three_days_weather_result_kb_builder,
)
from weather.three_days_weather.utils import get_weather_three_days

router = Router(name=__name__)


@router.callback_query(
    WeatherActionCb.filter(F.action == WeatherAction.three_days_weather),
    flags={"chat_action": "typing"},
)
async def ask_city(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await asyncio.sleep(0.2)
    await callback.message.edit_text(
        "Выбери город из предложенных или введи нужный",
        reply_markup=weather_three_days_kb_builder(),
    )
    await state.set_state(Weather.three_days_weather)


@router.callback_query(WeatherThreeDaysCb.filter(), flags={"chat_action": "typing"})
async def weather_three_days_cb(
    callback: CallbackQuery,
    callback_data: WeatherThreeDaysCb,
    state: FSMContext,
) -> None:
    await callback.answer()
    async with aiohttp.ClientSession() as http_session:
        weather = await get_weather_three_days(http_session, callback_data.city.value)
    if weather:
        await callback.answer()
        await callback.message.edit_text(
            weather,
            parse_mode="HTML",
            reply_markup=three_days_weather_result_kb_builder(as_edit=False),
        )
    else:
        await asyncio.sleep(0.2)
        await callback.message.edit_text(
            text=weather_error, reply_markup=main_menu_kb_builder()
        )
    await state.clear()


@router.message(Weather.three_days_weather, flags={"chat_action": "typing"})
async def weather_three_days(message: Message, state: FSMContext) -> None:
    await state.update_data(city=message.text)
    context_data = await state.get_data()
    city = context_data.get("city")
    async with aiohttp.ClientSession() as http_session:
        weather = await get_weather_three_days(http_session, city)
    if weather:
        await message.answer(
            weather,
            parse_mode="HTML",
            reply_markup=three_days_weather_result_kb_builder(as_edit=False),
        )
    else:
        await asyncio.sleep(0.2)
        await message.reply(text=weather_error, reply_markup=main_menu_kb_builder())
    await state.clear()
