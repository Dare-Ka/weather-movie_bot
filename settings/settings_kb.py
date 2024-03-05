from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

settings = [[KeyboardButton(text='Да')],
            [KeyboardButton(text='Нет')],
            [KeyboardButton(text='◀️ Выйти в меню')]]

settings_kb = ReplyKeyboardMarkup(keyboard=settings,
                                  resize_keyboard=True,
                                  one_time_keyboard=True)

menu_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Меню')]], resize_keyboard=True)
