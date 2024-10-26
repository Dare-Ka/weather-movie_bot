from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from main_menu.keyboard import MainMenuActionsCb, MainMenuActions, MainMenu, MainMenuCb


def meal_kb_builder() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔄 Повторить",
        callback_data=MainMenuActionsCb(action=MainMenuActions.meal).pack(),
    )
    builder.button(text="⬅️ Назад", callback_data=MainMenuCb(main=MainMenu.menu).pack())
    return builder.as_markup()
