from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
admin_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Рассылка сообщения",
                                                                       callback_data="mailing"),
                                                 InlineKeyboardButton(text="Сообщение пользователю",
                                                                      callback_data="send_message")],
                                                 [InlineKeyboardButton(text="Список пользователей",
                                                                       callback_data="get_users_list"),
                                                  InlineKeyboardButton(text="Удалить пользователя",
                                                                       callback_data="delete_user")],
                                                 [InlineKeyboardButton(text="Режим пользователя",
                                                                       callback_data="back")]])

iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])

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
                                                                   callback_data='create_event')]
                                              ]
                             )
