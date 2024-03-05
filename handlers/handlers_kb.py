from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

imenu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Погода⛅️',
                                                                    callback_data='weather_today'),
                                              InlineKeyboardButton(text='Подобрать фильм🎦',
                                                                   callback_data='get_random_movie')],
                                              [InlineKeyboardButton(text='Погода на 3 дня⛅️',
                                                                    callback_data='weather_three_days'),
                                              InlineKeyboardButton(text='Что за фильм?🎬',
                                                                   callback_data='movie_description')],
                                              [InlineKeyboardButton(text='Что на ужин🍽',
                                                                    callback_data='random_meal'),
                                              InlineKeyboardButton(text='Напомни мне📔',
                                                                   callback_data='create_event')],
                                              [InlineKeyboardButton(text='Настройки⚙️',
                                                                    callback_data='settings')]])

menu_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Меню')]], resize_keyboard=True)

imenu_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Меню', callback_data='menu')]])

iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])
