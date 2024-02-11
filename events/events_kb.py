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
                                                                   callback_data='get_random_meal'),
                                              InlineKeyboardButton(text='Напомни мне📔',
                                                                   callback_data='create_event')]])

menu_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Меню')]], resize_keyboard=True)

imenu_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Меню', callback_data='menu')]])

iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])

donate_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Поддержать проект💸',
                                                                        url='https://pay.cloudtips.ru/p/e14be36c')]])

times = [
    [KeyboardButton(text='1'),
     KeyboardButton(text='3')],
    [KeyboardButton(text='6'),
     KeyboardButton(text='8')],
    [KeyboardButton(text='10'),
     KeyboardButton(text='12')],
    [KeyboardButton(text='◀️ Выйти в меню')]
    ]
times_kb = ReplyKeyboardMarkup(keyboard=times,
                               resize_keyboard=True,
                               input_field_placeholder='Через сколько напомнить...',
                               one_time_keyboard=True)

reminder_back = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Напомни мне📔',
                                                                            callback_data='create_event')],
                                                      [InlineKeyboardButton(text="◀️ Выйти в меню",
                                                                            callback_data="menu")]])