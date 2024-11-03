from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from main_menu.keyboard import MainMenuCb, MainMenu


class AdminActions(str, Enum):
    mailing = "Рассылка сообщения"
    send_message = "Сообщение пользователю"
    get_users_list = "Список пользователей"
    delete_user = "Удалить пользователя"


class AdminActionsCb(CallbackData, prefix="admin"):
    action: AdminActions


def build_admin_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for action in AdminActions:
        builder.button(text=action, callback_data=AdminActionsCb(action=action))
    builder.button(text="⬅️ Назад", callback_data=MainMenuCb(main=MainMenu.menu).pack())
    builder.adjust(2)
    return builder.as_markup()
