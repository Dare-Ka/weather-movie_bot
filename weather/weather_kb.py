from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


cities = [[KeyboardButton(text='Санкт-Петербург')],
          [KeyboardButton(text='Казань')],
          [KeyboardButton(text='Екатеринбург')],
          [KeyboardButton(text='Москва')],
          [KeyboardButton(text='◀️ Выйти в меню')]]

cities_kb = ReplyKeyboardMarkup(keyboard=cities,
                                resize_keyboard=True,
                                input_field_placeholder='Введите город...',
                                one_time_keyboard=True)

url = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Яндекс Погода',
                                                                  url='https://yandex.ru/pogoda/find')]])
