import asyncio

import aiohttp
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.core.models import db_helper
from bot.main_menu.keyboard import main_menu_kb_builder
from bot.tools.keyboard import ToolsActionsCb, ToolsActions
from bot.weather.text import weather_error
from bot.weather.todays_weather.utils import get_weather_today
from core.schemas.users.crud import update_user, get_user
from core.schemas.users.schemas import UserUpdate
from .keyboard import (
    mailing_settings_actions_kb_builder,
    MailingSettingsActionsCb,
    mailing_cities_kb_builder,
    retry_mailing_settings,
)
from .state import MailingSettings

router = Router(name=__name__)


@router.callback_query(
    ToolsActionsCb.filter(F.action == ToolsActions.mailing_settings),
    flags={"chat_action": "typing"},
)
async def ask_settings(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        text="Привет! Настраиваем рассылку!" "Отправлять утренние/вечерние сообщения?",
        reply_markup=mailing_settings_actions_kb_builder(),
    )
    await asyncio.sleep(0.2)


@router.callback_query(
    MailingSettingsActionsCb.filter(F.action),
    flags={"chat_action": "typing"},
)
async def mailing_settings(
    callback: CallbackQuery,
    callback_data: MailingSettingsActionsCb,
    state: FSMContext,
):
    await state.clear()
    await callback.answer()
    mailing = callback_data.action.value
    if mailing.strip().lower() == "да":
        await asyncio.sleep(0.2)
        await callback.message.edit_text(
            "Выбери город для утренней рассылки погоды или введи свой",
            reply_markup=mailing_cities_kb_builder(),
        )
        await state.set_state(MailingSettings.city)
    elif mailing.strip().lower() == "нет":
        async with db_helper.get_session() as session:
            user = await get_user(session=session, tg_id=callback.from_user.id)
            user_update = UserUpdate(
                tg_id=callback.from_user.id,
                mailing=False,
                city=None,
            )
            await update_user(session=session, user=user, user_update=user_update)
        await callback.message.edit_text(
            text="Запомнил!\n" "Настройки в любой момент можно изменить😉",
            reply_markup=main_menu_kb_builder(),
        )


@router.callback_query(
    MailingSettingsActionsCb.filter(F.city),
    flags={"chat_action": "typing"},
)
async def set_mailing_city_with_cb(
    callback: CallbackQuery,
    callback_data: MailingSettingsActionsCb,
    state: FSMContext,
):
    await state.clear()
    await callback.answer()
    city = callback_data.city.value
    async with db_helper.get_session() as session:
        user = await get_user(session=session, tg_id=callback.from_user.id)
        user_update = UserUpdate(
            tg_id=callback.from_user.id,
            mailing=True,
            city=city,
        )
        await update_user(session=session, user=user, user_update=user_update)
    await callback.message.edit_text(
        text="Запомнил!\n" "Настройки в любой момент можно изменить😉",
        reply_markup=main_menu_kb_builder(),
    )


@router.message(MailingSettings.city, flags={"chat_action": "typing"})
async def set_mailing_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    context_date = await state.get_data()
    city = context_date.get("city")
    async with aiohttp.ClientSession() as http_session:
        weather = await get_weather_today(http_session=http_session, city=city)
    if weather:
        async with db_helper.get_session() as session:
            user = await get_user(session=session, tg_id=message.from_user.id)
            user_update = UserUpdate(
                tg_id=message.from_user.id,
                mailing=True,
                city=city,
            )
            await update_user(session=session, user=user, user_update=user_update)
        await message.answer(
            text="Запомнил!\n" "Настройки в любой момент можно изменить😉",
            reply_markup=main_menu_kb_builder(),
        )
        await state.clear()
    else:
        await message.answer(
            text=weather_error + "\nПопробуем еще?",
            reply_markup=retry_mailing_settings(),
        )
