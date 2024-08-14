from events.events_text import good_morning_text, good_night_text, good_night_stickers, good_morning_stickers, donate_schedule, love_sticker, good_vacation_text, genres, movie_mailing_text
import config
from events.events_kb import menu_kb, iexit_kb, donate_kb
from movie.movie_utils import get_random_movie
from weather.weather_kb import url
from weather.weather_utils import get_weather_today
from db.models import db
from admin.admin import error_handler
from random import choice
import asyncio
from aiogram import Bot, types
from aiogram.exceptions import AiogramError


async def reminder(name: str, tg_id: int, event: str, bot: Bot) -> None:
    """Send scheduled notification to users"""
    try:
        await bot.send_message(chat_id=tg_id,
                               text=f'{name}, напоминаю тебе:\n\n' + event,
                               reply_markup=iexit_kb)
    except AiogramError as error:
        await error_handler('reminder:' + str(error), bot)
        if str(error) == 'Telegram server says - Forbidden: bot was blocked by the user':
            await error_handler(error=f'Проблема с пользователем:\n'
                                      f'Имя: {tg_id}\n'
                                      f'ID: {tg_id}\n',
                                bot=bot)
            await db.delete_user(tg_id)
            await bot.send_message(chat_id=config.ADMIN_ID, text='Пользователь удален!')


async def good_morning(bot: Bot) -> None:
    """Send morning scheduled notification to users"""
    for tg_id, tg_name, city in await db.get_mailing_users():
        try:
            await bot.send_message(chat_id=tg_id,
                                   text=choice(good_morning_text).format(name=tg_name)
                                   )
            await bot.send_sticker(chat_id=tg_id,
                                   sticker=choice(good_morning_stickers),
                                   reply_markup=menu_kb
                                   )
            if city:
                weather = await get_weather_today(city)
                await bot.send_message(chat_id=tg_id,
                                       text=weather,
                                       reply_markup=url,
                                       parse_mode='HTML')
                await asyncio.sleep(0.1)
        except AiogramError as error:
            await error_handler(str(error), bot)
            if str(error) == 'Telegram server says - Forbidden: bot was blocked by the user':
                await error_handler(error=f'Проблема с пользователем:\n'
                                          f'Имя: {tg_name}\n'
                                          f'ID: {tg_id}', bot=bot)
                await db.delete_user(tg_id)
                await bot.send_message(chat_id=config.ADMIN_ID, text='Пользователь удален!')
            await asyncio.sleep(0.1)


async def good_night(bot: Bot) -> None:
    """Send night scheduled notification to users"""
    for tg_id, tg_name, city in await db.get_mailing_users():
        try:
            await bot.send_message(chat_id=tg_id,
                                   text=choice(good_night_text).format(name=tg_name))
            await bot.send_sticker(chat_id=tg_id,
                                   sticker=choice(good_night_stickers))
            await asyncio.sleep(0.1)
        except AiogramError as error:
            await error_handler(str(error), bot)
            if str(error) == 'Telegram server says - Forbidden: bot was blocked by the user':
                await error_handler(error=f'Проблема с пользователем:\n'
                                          f'Имя: {tg_name}\n'
                                          f'ID: {tg_id}',
                                    bot=bot)
                await db.delete_user(tg_id)
                await bot.send_message(chat_id=config.ADMIN_ID, text='Пользователь удален!')
            await asyncio.sleep(0.1)


async def movie_mailing(bot: Bot) -> None:
    """Send random movie to users"""
    res= await get_random_movie(genre_name=choice(genres))
    for tg_id, tg_name, city in await db.get_mailing_users():
        try:
            await bot.send_message(chat_id=tg_id,
                                   text=movie_mailing_text)
            await bot.send_photo(chat_id=tg_id,
                                 photo=res[3],
                                 caption=res[0],
                                 reply_markup=menu_kb,
                                 parse_mode='HTML')
            if len(res[2]) != 0:
                await bot.send_message(chat_id=tg_id,
                                       text='Не понял описание? Посмотри трейлер🔥',
                                       reply_markup=res[1])
            await asyncio.sleep(0.1)
        except AiogramError as error:
            await error_handler(str(error), bot)
            if str(error) == 'Telegram server says - Forbidden: bot was blocked by the user':
                await error_handler(error=f'Проблема с пользователем:\n'
                                          f'Имя: {tg_name}\n'
                                          f'ID: {tg_id}',
                                    bot=bot)
                await db.delete_user(tg_id)
                await bot.send_message(chat_id=config.ADMIN_ID, text='Пользователь удален!')
            await asyncio.sleep(0.1)


async def good_vacation(bot: Bot) -> None:
    """Send vacation scheduled notification to users"""
    for tg_id, tg_name, city in await db.get_mailing_users():
        try:
            await bot.send_message(chat_id=tg_id,
                                   text=choice(good_vacation_text).format(name=tg_name)
                                   )
            await bot.send_sticker(chat_id=tg_id,
                                   sticker=choice(good_morning_stickers),
                                   reply_markup=menu_kb
                                   )
            if city:
                weather = await get_weather_today(city)
                await bot.send_message(chat_id=tg_id,
                                       text=weather,
                                       reply_markup=url,
                                       parse_mode='HTML')
            await asyncio.sleep(0.1)
        except AiogramError as error:
            await error_handler(str(error), bot)
            if str(error) == 'Telegram server says - Forbidden: bot was blocked by the user':
                await error_handler(error=f'Проблема с пользователем:\n'
                                          f'Имя: {tg_name}\n'
                                          f'ID: {tg_id}',
                                    bot=bot)
                await db.delete_user(tg_id)
                await bot.send_message(chat_id=config.ADMIN_ID, text='Пользователь удален!')
            await asyncio.sleep(0.1)


async def happy_ny(bot: Bot) -> None:
    """Send congratulation scheduled notification to users"""
    for tg_id in await db.get_users_info():
        try:
            NY_picture = types.FSInputFile(r'/my_bots/Harper/events/HappyNY.jpg')
            await bot.send_photo(chat_id=tg_id[0],
                                 photo=NY_picture,
                                 caption=f'{tg_id[1]},с Новым Годом тебя!!!❤️☃️❄️\n'
                                         f'Пусть этот год будет переполнен только приятными событиями!')
            await asyncio.sleep(0.1)
        except AiogramError as error:
            await error_handler(str(error), bot)
            if str(error) == 'Telegram server says - Forbidden: bot was blocked by the user':
                await error_handler(error=f'Проблема с пользователем:\nИ'
                                          f'мя: {tg_id[1]}\n'
                                          f'ID: {tg_id[0]}\n'
                                          f'username: {tg_id[2]}',
                                    bot=bot)
                await db.delete_user(tg_id[0])
                await bot.send_message(chat_id=config.ADMIN_ID, text='Пользователь удален!')
            await asyncio.sleep(0.1)


async def donate(bot: Bot) -> None:
    """Send scheduled notification about donation to users"""
    for tg_id in await db.get_users_info():
        try:
            await bot.send_message(chat_id=tg_id[0],
                                   text=donate_schedule,
                                   reply_markup=donate_kb)
            await bot.send_sticker(chat_id=tg_id[0],
                                   sticker=choice(love_sticker))
            await asyncio.sleep(0.1)
        except AiogramError as error:
            await error_handler(str(error), bot)
            if str(error) == 'Telegram server says - Forbidden: bot was blocked by the user':
                await error_handler(error=f'Проблема с пользователем:\n'
                                          f'Имя: {tg_id[1]}\n'
                                          f'ID: {tg_id[0]}\n'
                                          f'username: {tg_id[2]}', bot=bot)
                await db.delete_user(tg_id[0])
                await bot.send_message(chat_id=config.ADMIN_ID, text='Пользователь удален!')
            await asyncio.sleep(0.1)
