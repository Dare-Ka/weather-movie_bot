from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

meal_back = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Придумай ужин🍽',
                                                                        callback_data='random_meal')],
                                                  [InlineKeyboardButton(text="◀️ Выйти в меню",
                                                                        callback_data="menu")]])

