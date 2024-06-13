from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

settings = [[KeyboardButton(text='Да')],
            [KeyboardButton(text='Нет')],
            [KeyboardButton(text='◀️ Выйти в меню')]]

settings_kb = ReplyKeyboardMarkup(keyboard=settings,
                                  resize_keyboard=True,
                                  one_time_keyboard=True)

menu_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Меню')]], resize_keyboard=True)

again = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Настройки⚙️', callback_data='settings')]])