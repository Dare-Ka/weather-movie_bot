from pathlib import Path
from random import choice

import aiohttp
from aiogram import Bot, types
from aiogram.exceptions import TelegramForbiddenError

import bot.core.scheduler.text as text
from bot.core.config import settings
from bot.core.models import db_helper
from bot.main_menu.keyboard import main_menu_kb_builder
from bot.movie.random_movie.keyboard import trailers_kb_builder
from bot.movie.random_movie.utils import get_random_movie
from bot.weather.todays_weather.keyboard import weather_today_result_kb_builder
from bot.weather.todays_weather.utils import get_weather_today
from core.schemas.users.crud import get_users, get_mailing_users, get_user, update_user
from core.schemas.users.schemas import UserUpdate


async def good_morning(bot: Bot) -> None:
    """Send morning scheduled notification to users"""
    async with db_helper.get_session() as session:
        users = await get_mailing_users(session=session)
    for user in users:
        try:
            await bot.send_message(
                chat_id=user.tg_id,
                text=choice(text.good_morning_text).format(name=user.tg_name),
            )
            await bot.send_sticker(
                chat_id=user.tg_id,
                sticker=choice(text.good_morning_stickers),
                reply_markup=main_menu_kb_builder(as_edit=False),
            )
            if user.city:
                async with aiohttp.ClientSession() as http_session:
                    weather = await get_weather_today(http_session, user.city)
                await bot.send_message(
                    chat_id=user.tg_id,
                    text=weather,
                    reply_markup=weather_today_result_kb_builder(as_edit=False),
                    parse_mode="HTML",
                )
        except TelegramForbiddenError:
            async with db_helper.get_session() as session:
                found_user = await get_user(session=session, tg_id=user.tg_id)
                user_update = UserUpdate(
                    tg_id=user.tg_id,
                    mailing=False,
                    active=False,
                )
                await update_user(
                    session=session, user=found_user, user_update=user_update
                )
            await bot.send_message(
                chat_id=settings.bot.admin_id,
                text=f"Пользователь c id {user.tg_id} деактивирован!",
            )


async def good_night(bot: Bot) -> None:
    """Send night scheduled notification to users"""
    async with db_helper.get_session() as session:
        users = await get_mailing_users(session=session)
    for user in users:
        try:
            await bot.send_message(
                chat_id=user.tg_id,
                text=choice(text.good_night_text).format(name=user.tg_name),
            )
            await bot.send_sticker(
                chat_id=user.tg_id,
                sticker=choice(text.good_night_stickers),
            )
        except TelegramForbiddenError:
            async with db_helper.get_session() as session:
                found_user = await get_user(session=session, tg_id=user.tg_id)
                user_update = UserUpdate(
                    tg_id=user.tg_id,
                    mailing=False,
                    active=False,
                )
                await update_user(
                    session=session, user=found_user, user_update=user_update
                )
            await bot.send_message(
                chat_id=settings.bot.admin_id,
                text=f"Пользователь c id {user.tg_id} деактивирован!",
            )


async def movie_mailing(bot: Bot) -> None:
    """Send random movie to users"""
    async with aiohttp.ClientSession() as http_session:
        while True:
            movie = await get_random_movie(
                http_session,
                genre_name=choice(text.genres),
            )
            if movie:
                break
    async with db_helper.get_session() as session:
        users = await get_mailing_users(session=session)
    for user in users:
        try:
            await bot.send_message(
                chat_id=user.tg_id,
                text=text.movie_mailing_text,
            )
            await bot.send_photo(
                chat_id=user.tg_id,
                photo=movie[2],
                caption=movie[0],
                reply_markup=trailers_kb_builder(movie[1]),
                parse_mode="HTML",
            )
        except TelegramForbiddenError:
            async with db_helper.get_session() as session:
                found_user = await get_user(session=session, tg_id=user.tg_id)
                user_update = UserUpdate(
                    tg_id=user.tg_id,
                    mailing=False,
                    active=False,
                )
                await update_user(
                    session=session, user=found_user, user_update=user_update
                )
            await bot.send_message(
                chat_id=settings.bot.admin_id,
                text=f"Пользователь c id {user.tg_id} деактивирован!",
            )


async def good_vacation(bot: Bot) -> None:
    """Send vacation scheduled notification to users"""
    async with db_helper.get_session() as session:
        users = await get_mailing_users(session=session)
    for user in users:
        try:
            await bot.send_message(
                chat_id=user.tg_id,
                text=choice(text.good_vacation_text).format(name=user.tg_name),
            )
            await bot.send_sticker(
                chat_id=user.tg_id,
                sticker=choice(text.good_morning_stickers),
                reply_markup=main_menu_kb_builder(as_edit=False),
            )
            if user.city:
                async with aiohttp.ClientSession() as http_session:
                    weather = await get_weather_today(http_session, user.city)
                await bot.send_message(
                    chat_id=user.tg_id,
                    text=weather,
                    reply_markup=weather_today_result_kb_builder(as_edit=False),
                    parse_mode="HTML",
                )
        except TelegramForbiddenError:
            async with db_helper.get_session() as session:
                found_user = await get_user(session=session, tg_id=user.tg_id)
                user_update = UserUpdate(
                    tg_id=user.tg_id,
                    mailing=False,
                    active=False,
                )
                await update_user(
                    session=session, user=found_user, user_update=user_update
                )
            await bot.send_message(
                chat_id=settings.bot.admin_id,
                text=f"Пользователь c id {user.tg_id} деактивирован!",
            )


async def happy_ny(bot: Bot) -> None:
    """Send congratulation scheduled notification to users"""
    ny_picture_path = Path(__file__).parent / "happyNY.png"
    async with db_helper.get_session() as session:
        users = await get_users(session=session)
    for user in users:
        try:
            ny_picture = types.FSInputFile(ny_picture_path)
            await bot.send_photo(
                chat_id=user.tg_id,
                photo=ny_picture,
                caption=f"{user.tg_name}, с Новым Годом тебя!!!❤️☃️❄️\n"
                f"Пусть этот год будет переполнен только приятными событиями!",
                reply_markup=main_menu_kb_builder(as_edit=False),
            )
        except TelegramForbiddenError:
            async with db_helper.get_session() as session:
                found_user = await get_user(session=session, tg_id=user.tg_id)
                user_update = UserUpdate(
                    tg_id=user.tg_id,
                    mailing=False,
                    active=False,
                )
                await update_user(
                    session=session, user=found_user, user_update=user_update
                )
            await bot.send_message(
                chat_id=settings.bot.admin_id,
                text=f"Пользователь c id {user.tg_id} деактивирован!",
            )
