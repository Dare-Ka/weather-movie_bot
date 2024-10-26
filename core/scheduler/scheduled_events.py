from pathlib import Path
from random import choice

import aiohttp
from aiogram import Bot, types
from aiogram.exceptions import TelegramForbiddenError

import core.scheduler.text as text
from admin.errors import error_notifier
from core.config import settings
from db.models import db
from main_menu.keyboard import main_menu_actions_kb_builder
from movie.random_movie.keyboard import trailers_kb_builder
from movie.random_movie.utils import get_random_movie
from weather.todays_weather.keyboard import weather_today_result_kb_builder
from weather.todays_weather.utils import get_weather_today


async def good_morning(bot: Bot) -> None:
    """Send morning scheduled notification to users"""
    for tg_id, tg_name, city in await db.get_mailing_users():
        try:
            await bot.send_message(
                chat_id=tg_id, text=choice(text.good_morning_text).format(name=tg_name)
            )
            await bot.send_sticker(
                chat_id=tg_id,
                sticker=choice(text.good_morning_stickers),
                reply_markup=main_menu_actions_kb_builder(),
            )
            if city:
                async with aiohttp.ClientSession() as http_session:
                    weather = await get_weather_today(http_session, city)
                await bot.send_message(
                    chat_id=tg_id,
                    text=weather,
                    reply_markup=weather_today_result_kb_builder(as_edit=False),
                    parse_mode="HTML",
                )
        except TelegramForbiddenError as error:
            await error_notifier(func_name=good_morning.__name__, error=error)
            await db.delete_user(tg_id)
            await bot.send_message(
                chat_id=settings.ADMIN_ID,
                text=f"Пользователь c id {tg_id} удален!",
            )


async def good_night(bot: Bot) -> None:
    """Send night scheduled notification to users"""
    for tg_id, tg_name, city in await db.get_mailing_users():
        try:
            await bot.send_message(
                chat_id=tg_id,
                text=choice(text.good_night_text).format(name=tg_name),
            )
            await bot.send_sticker(
                chat_id=tg_id,
                sticker=choice(text.good_night_stickers),
            )
        except TelegramForbiddenError as error:
            await error_notifier(func_name=good_morning.__name__, error=error)
            await db.delete_user(tg_id)
            await bot.send_message(
                chat_id=settings.ADMIN_ID,
                text=f"Пользователь c id {tg_id} удален!",
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
    for tg_id, tg_name, city in await db.get_mailing_users():
        try:
            await bot.send_message(
                chat_id=tg_id,
                text=text.movie_mailing_text,
            )
            await bot.send_photo(
                chat_id=tg_id,
                photo=movie[2],
                caption=movie[0],
                reply_markup=trailers_kb_builder(movie[1]),
                parse_mode="HTML",
            )
        except TelegramForbiddenError as error:
            await error_notifier(
                func_name=good_morning.__name__,
                error=error,
            )
            await db.delete_user(tg_id)
            await bot.send_message(
                chat_id=settings.ADMIN_ID,
                text=f"Пользователь c id {tg_id} удален!",
            )


async def good_vacation(bot: Bot) -> None:
    """Send vacation scheduled notification to users"""
    for tg_id, tg_name, city in await db.get_mailing_users():
        try:
            await bot.send_message(
                chat_id=tg_id, text=choice(text.good_vacation_text).format(name=tg_name)
            )
            await bot.send_sticker(
                chat_id=tg_id,
                sticker=choice(text.good_morning_stickers),
                reply_markup=main_menu_actions_kb_builder(),
            )
            if city:
                async with aiohttp.ClientSession() as http_session:
                    weather = await get_weather_today(http_session, city)
                await bot.send_message(
                    chat_id=tg_id,
                    text=weather,
                    reply_markup=weather_today_result_kb_builder(as_edit=False),
                    parse_mode="HTML",
                )
        except TelegramForbiddenError as error:
            await error_notifier(func_name=good_morning.__name__, error=error)
            await db.delete_user(tg_id)
            await bot.send_message(
                chat_id=settings.ADMIN_ID,
                text=f"Пользователь c id {tg_id} удален!",
            )


async def happy_ny(bot: Bot) -> None:
    """Send congratulation scheduled notification to users"""
    ny_picture_path = Path(__file__).parent / "HappyNY.jpg"
    for tg_id in await db.get_users_info():
        try:
            ny_picture = types.FSInputFile(ny_picture_path)
            await bot.send_photo(
                chat_id=tg_id[0],
                photo=ny_picture,
                caption=f"{tg_id[1]},с Новым Годом тебя!!!❤️☃️❄️\n"
                f"Пусть этот год будет переполнен только приятными событиями!",
                reply_markup=main_menu_actions_kb_builder(),
            )
        except TelegramForbiddenError as error:
            await error_notifier(func_name=good_morning.__name__, error=error)
            await db.delete_user(tg_id)
            await bot.send_message(
                chat_id=settings.ADMIN_ID,
                text=f"Пользователь c id {tg_id} удален!",
            )
