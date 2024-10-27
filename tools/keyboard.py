from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from main_menu.keyboard import MainMenuCb, MainMenu


class ToolsActions(str, Enum):
    create_event = "⏰ Напомни мне"
    send_message = "✍️ Отправить сообщение"
    todo_list = "📝 Список дел"
    mailing_settings = "⚙️ Настройки"


class ToolsActionsCb(CallbackData, prefix="tools"):
    action: ToolsActions


def tools_kb_builder() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for action in ToolsActions:
        builder.button(text=action.value, callback_data=ToolsActionsCb(action=action))
    builder.button(
        text="⬅️ Назад",
        callback_data=MainMenuCb(main=MainMenu.menu).pack(),
    )
    builder.adjust(1)
    return builder.as_markup()
