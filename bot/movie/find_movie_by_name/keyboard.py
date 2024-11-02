from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.main_menu.keyboard import (
    MainMenu,
    MainMenuCb,
    MainMenuActionsCb,
    MainMenuActions,
)


def find_movie_actions_kb_builder() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="⬅️ Назад",
        callback_data=MainMenuActionsCb(action=MainMenuActions.movie).pack(),
    )
    builder.adjust(1)
    return builder.as_markup()


def find_movie_by_name_result_kb_builder(
    link_kb: InlineKeyboardMarkup, as_edit: bool = True
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.attach(InlineKeyboardBuilder.from_markup(link_kb))
    builder.button(
        text=MainMenu.menu.value,
        callback_data=MainMenuCb(main=MainMenu.menu, as_edit=as_edit).pack(),
    )
    builder.adjust(2)
    return builder.as_markup()
