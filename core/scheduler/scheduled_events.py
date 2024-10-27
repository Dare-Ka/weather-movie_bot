from pathlib import Path
from random import choice

import aiohttp
from aiogram import Bot, types
from aiogram.exceptions import TelegramForbiddenError

import core.scheduler.text as text
from core.config import settings
from core.models import db_helper
from database.users.crud import get_users, delete_user, get_mailing_users
from main_menu.keyboard import main_menu_actions_kb_builder
from movie.random_movie.keyboard import trailers_kb_builder
from movie.random_movie.utils import get_random_movie
from weather.todays_weather.keyboard import weather_today_result_kb_builder
from weather.todays_weather.utils import get_weather_today


async def good_morning(bot: Bot) -> None:
    """Send morning scheduled notification to users"""
    session = await db_helper.get_scoped_session()
    for user in await get_mailing_users(session=session):
        try:
            await bot.send_message(
                chat_id=user.tg_id,
                text=choice(text.good_morning_text).format(name=user.tg_name),
            )
            await bot.send_sticker(
                chat_id=user.tg_id,
                sticker=choice(text.good_morning_stickers),
                reply_markup=main_menu_actions_kb_builder(),
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
            await delete_user(session=session, user=user)
            await bot.send_message(
                chat_id=settings.ADMIN_ID,
                text=f"Пользователь c id {user.tg_id} удален!",
            )


async def good_night(bot: Bot) -> None:
    """Send night scheduled notification to users"""
    session = await db_helper.get_scoped_session()
    for user in await get_mailing_users(session=session):
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
            await delete_user(session=session, user=user)
            await bot.send_message(
                chat_id=settings.ADMIN_ID,
                text=f"Пользователь c id {user.tg_id} удален!",
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
    session = await db_helper.get_scoped_session()
    for user in await get_mailing_users(session=session):
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
            await delete_user(session=session, user=user)
            await bot.send_message(
                chat_id=settings.ADMIN_ID,
                text=f"Пользователь c id {user.tg_id} удален!",
            )


async def good_vacation(bot: Bot) -> None:
    """Send vacation scheduled notification to users"""
    session = await db_helper.get_scoped_session()
    for user in await get_mailing_users(session=session):
        try:
            await bot.send_message(
                chat_id=user.tg_id,
                text=choice(text.good_vacation_text).format(name=user.tg_name),
            )
            await bot.send_sticker(
                chat_id=user.tg_id,
                sticker=choice(text.good_morning_stickers),
                reply_markup=main_menu_actions_kb_builder(),
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
            await delete_user(session=session, user=user)
            await bot.send_message(
                chat_id=settings.ADMIN_ID,
                text=f"Пользователь c id {user.tg_id} удален!",
            )


async def happy_ny(bot: Bot) -> None:
    """Send congratulation scheduled notification to users"""
    ny_picture_path = Path(__file__).parent / "HappyNY.jpg"
    session = await db_helper.get_scoped_session()
    for user in await get_users(session=session):
        try:
            ny_picture = types.FSInputFile(ny_picture_path)
            await bot.send_photo(
                chat_id=user.tg_id,
                photo=ny_picture,
                caption=f"{user.tg_name},с Новым Годом тебя!!!❤️☃️❄️\n"
                f"Пусть этот год будет переполнен только приятными событиями!",
                reply_markup=main_menu_actions_kb_builder(),
            )
        except TelegramForbiddenError:
            await delete_user(session=session, user=user)
            await bot.send_message(
                chat_id=settings.ADMIN_ID,
                text=f"Пользователь c id {user.tg_id} удален!",
            )
