from admin.admin import error_handler
from weather.weather_utils import get_weather_today, get_weather_three_days
from weather.weather_kb import cities, url
from weather.weather_text import weather_error
from settings.states import Gen
from handlers.handlers_kb import menu_kb, iexit_kb
from db.db import update_user
import asyncio
from aiogram import types, F, Bot, Router
from aiogram.fsm.context import FSMContext

router = Router()


@router.callback_query(F.data == 'weather_today', flags={'chat_action': 'typing'})
async def ask_city(callback: types.CallbackQuery, state: FSMContext):
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
    await state.set_state(Gen.weather_today)
    await asyncio.sleep(0.2)
    await callback.message.answer("Привет, рад тебя видеть! Выбери город из предложенных или введи нужный",
                                  reply_markup=cities)


@router.message(Gen.weather_today, flags={'chat_action': 'typing'})
async def weather_today(message: types.Message, state: FSMContext, bot: Bot):
    try:
        await state.update_data(city=message.text)
        context_data = await state.get_data()
        city = context_data.get('city')
        res = await get_weather_today(city)
        if len(res) == 0:
            await asyncio.sleep(0.2)
            await message.reply(weather_error, reply_markup=iexit_kb)
            await state.clear()
        await asyncio.sleep(0.2)
        await message.answer(res, parse_mode="HTML", reply_markup=menu_kb)
        await message.answer('Если нужно подробнее:', reply_markup=url)
        await state.clear()
    except Exception as error:
        await error_handler('get_weather_today:\n' + str(error), bot)
        await state.clear()


@router.callback_query(F.data == 'weather_three_days', flags={'chat_action': 'typing'})
async def ask_city(callback: types.CallbackQuery, state: FSMContext):
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
    await state.set_state(Gen.three_days_weather)
    await asyncio.sleep(0.2)
    await callback.message.answer("Привет, рад тебя видеть! Выбери город из предложенных или введи нужный",
                                  reply_markup=cities)


@router.message(Gen.three_days_weather, flags={'chat_action': 'typing'})
async def weather_three_days(message: types.Message, state: FSMContext, bot: Bot):
    try:
        await state.update_data(city=message.text)
        context_data = await state.get_data()
        city = context_data.get('city')
        res = await get_weather_three_days(city)
        if res is None:
            await asyncio.sleep(0.2)
            await message.reply(weather_error, reply_markup=iexit_kb)
            await state.clear()
        await asyncio.sleep(0.2)
        await message.answer(res[0], parse_mode="HTML", reply_markup=menu_kb)
        await asyncio.sleep(0.3)
        await message.answer(res[1], parse_mode="HTML")
        await asyncio.sleep(0.3)
        await message.answer(res[2], parse_mode="HTML")
        await message.answer('Если нужно подробнее:', reply_markup=url)
        await state.clear()
    except Exception as error:
        await error_handler('get_weather_three_days:\n' + str(error), bot)
        await state.clear()
