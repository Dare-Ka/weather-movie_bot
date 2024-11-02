from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MainMenu(str, Enum):
    menu = "📍 Главное меню"


class MainMenuCb(CallbackData, prefix="main_menu"):
    main: MainMenu
    as_edit: bool = True


class MainMenuActions(str, Enum):
    weather = "Погода ⛅️"
    movie = "Фильмы 🎬"
    tools = "Инструменты 🛠️"
    meal = "Что на ужин 🍽"


class MainMenuActionsCb(CallbackData, prefix="main_menu_actions"):
    action: MainMenuActions


def main_menu_kb_builder(as_edit: bool = True) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=MainMenu.menu.value,
        callback_data=MainMenuCb(main=MainMenu.menu, as_edit=as_edit).pack(),
    )
    builder.adjust(1)
    return builder.as_markup()


def main_menu_actions_kb_builder() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for action in MainMenuActions:
        builder.button(text=action, callback_data=MainMenuActionsCb(action=action))
    builder.adjust(2)
    return builder.as_markup()
