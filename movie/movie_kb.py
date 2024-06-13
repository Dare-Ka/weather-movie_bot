from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

random_movie_back = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Подобрать фильм🎦',
                                                                                callback_data='get_random_movie')],
                                                          [InlineKeyboardButton(text="◀️ Выйти в меню",
                                                                                callback_data="menu")]])

movie_genres = [
    [KeyboardButton(text='Комедия')],
    [KeyboardButton(text='Драма')],
    [KeyboardButton(text='Триллер')],
    [KeyboardButton(text='Детектив')],
    [KeyboardButton(text='Фантастика')],
    [KeyboardButton(text='◀️ Выйти в меню')]
    ]
movie_genres = ReplyKeyboardMarkup(keyboard=movie_genres,
                                   resize_keyboard=True,
                                   input_field_placeholder='Введите жанр...',
                                   one_time_keyboard=True)

movie_types = [
    [KeyboardButton(text='Кинофильм')],
    [KeyboardButton(text='TV-сериал')],
    [KeyboardButton(text='Мультфильм')],
    [KeyboardButton(text='Мультсериал')],
    [KeyboardButton(text='Аниме')],
    [KeyboardButton(text='◀️ Выйти в меню')]
]
movie_types_kb = ReplyKeyboardMarkup(keyboard=movie_types,
                                     resize_keyboard=True,
                                     one_time_keyboard=True)