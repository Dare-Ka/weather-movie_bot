from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from main_menu.keyboard import MainMenuCb, MainMenu


class MovieActions(str, Enum):
    find_movie_by_name = "🎦 Что за фильм?"
    random_movie = "🎬 Подобрать фильм"


class MovieActionsCb(CallbackData, prefix="movie"):
    action: MovieActions


def movie_actions_kb_builder() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for action in MovieActions:
        builder.button(text=action, callback_data=MovieActionsCb(action=action))
    builder.button(text="⬅️ Назад", callback_data=MainMenuCb(main=MainMenu.menu).pack())
    builder.adjust(2)
    return builder.as_markup()
