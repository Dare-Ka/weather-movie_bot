from events.events_text import good_morning_text, good_night_text, good_night_stickers, good_morning_stickers, donate_schedule, love_sticker, good_vacation_text
from events.events_kb import menu_kb, iexit_kb, donate_kb
from weather.weather_utils import get_weather_today
from db.db import get_users_info, delete_user
from admin.admin import error_handler
from random import choice
from aiogram import Bot
from aiogram.exceptions import AiogramError
import os


async def reminder(name: str, tg_id: int, event: str, bot: Bot) -> None:
    """Send scheduled notification to users"""
    try:
        await bot.send_message(chat_id=tg_id,
                               text=f'{name}, напоминаю тебе:\n\n' + event,
                               reply_markup=iexit_kb)
    except AiogramError as error:
        await error_handler('reminder:' + str(error), bot)


async def good_morning(bot: Bot) -> None:
    """Send morning scheduled notification to users"""
    for tg_id in await get_users_info():
        try:
            if tg_id[3] == 1:
                await bot.send_message(chat_id=tg_id[0],
                                       text=choice(good_morning_text).format(name=tg_id[1])
                                       )
                await bot.send_sticker(chat_id=tg_id[0],
                                       sticker=choice(good_morning_stickers),
                                       reply_markup=menu_kb
                                       )
                weather = await get_weather_today(tg_id[4])
                if len(weather) != 0:
                    await bot.send_message(chat_id=tg_id[0],
                                           text=weather,
                                           parse_mode='HTML')
        except AiogramError as error:
            await error_handler(str(error), bot)
            await error_handler(error=f'Проблаема с пользователем:\n'
                                      f'Имя: {tg_id[1]}\n'
                                      f'ID: {tg_id[0]}\n'
                                      f'username: {tg_id[2]}', bot=bot)
            await delete_user(tg_id[0])
            await bot.send_message(chat_id=int(os.getenv('ADMIN_ID')), text='Пользователь удален!')


async def good_night(bot: Bot) -> None:
    """Send night scheduled notification to users"""
    for tg_id in await get_users_info():
        try:
            if tg_id[3] == 1:
                await bot.send_message(chat_id=tg_id[0],
                                       text=choice(good_night_text).format(name=tg_id[1]))
                await bot.send_sticker(chat_id=tg_id[0],
                                       sticker=choice(good_night_stickers))
        except AiogramError as error:
            await error_handler(str(error), bot)
            await error_handler(error=f'Проблаема с пользователем:\nИмя: {tg_id[1]}\n'
                                      f'ID: {tg_id[0]}\n'
                                      f'username: {tg_id[2]}', bot=bot)
            await delete_user(tg_id[0])
            await bot.send_message(chat_id=int(os.getenv('ADMIN_ID')), text='Пользователь удален!')


async def good_vacation(bot: Bot) -> None:
    """Send vacation scheduled notification to users"""
    for tg_id in await get_users_info():
        try:
            if tg_id[3] == 1:
                await bot.send_message(chat_id=tg_id[0],
                                       text=choice(good_vacation_text).format(name=tg_id[1])
                                       )
                await bot.send_sticker(chat_id=tg_id[0],
                                       sticker=choice(good_morning_stickers),
                                       reply_markup=menu_kb
                                       )
                weather = await get_weather_today(tg_id[4])
                if len(weather) != 0:
                    await bot.send_message(chat_id=tg_id[0],
                                           text=weather,
                                           parse_mode='HTML')
        except AiogramError as error:
            await error_handler(str(error), bot)
            await error_handler(error=f'Проблаема с пользователем:\n'
                                      f'Имя: {tg_id[1]}\n'
                                      f'ID: {tg_id[0]}\n'
                                      f'username: {tg_id[2]}', bot=bot)
            await delete_user(tg_id[0])
            await bot.send_message(chat_id=int(os.getenv('ADMIN_ID')), text='Пользователь удален!')


async def happy_ny(bot: Bot) -> None:
    """Send congratulation scheduled notification to users"""
    for tg_id in await get_users_info():
        try:
            await bot.send_message(chat_id=tg_id[0],
                                   text=f'{tg_id[1]},с Новым Годом тебя!!!❤️☃️❄️\n'
                                        f'Пусть этот год будет переполнен только приятными событиями!')
            await bot.send_sticker(chat_id=tg_id,
                                   sticker=r'CAACAgIAAxkBAAEKpyhlQe_P0tmDDeo-54CoN6zuXsXzzAACOgADobYRCBvFr5Ov1gHjMwQ')
        except AiogramError as error:
            await error_handler(str(error), bot)
            await error_handler(error=f'Проблаема с пользователем:\nИмя: {tg_id[1]}\n'
                                      f'ID: {tg_id[0]}\n'
                                      f'username: {tg_id[2]}', bot=bot)
            await delete_user(tg_id[0])
            await bot.send_message(chat_id=int(os.getenv('ADMIN_ID')), text='Пользователь удален!')


async def donate(bot: Bot) -> None:
    """Send scheduled notification about donation to users"""
    for tg_id in await get_users_info():
        try:
            await bot.send_message(chat_id=tg_id[0],
                                   text=donate_schedule,
                                   reply_markup=donate_kb)
            await bot.send_sticker(chat_id=tg_id[0],
                                   sticker=choice(love_sticker))
        except AiogramError as error:
            await error_handler(str(error), bot)
            await error_handler(error=f'Проблаема с пользователем:\nИмя: {tg_id[1]}\n'
                                      f'ID: {tg_id[0]}\n'
                                      f'username: {tg_id[2]}', bot=bot)
            await delete_user(tg_id[0])
            await bot.send_message(chat_id=int(os.getenv('ADMIN_ID')), text='Пользователь удален!')
