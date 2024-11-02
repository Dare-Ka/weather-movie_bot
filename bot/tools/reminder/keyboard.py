from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.main_menu.keyboard import MainMenuActionsCb, MainMenuActions
from bot.tools.keyboard import ToolsActionsCb, ToolsActions


class Hours(Enum):
    ZERO = "0"
    ONE = "1"
    THREE = "3"
    SIX = "6"
    TEN = "10"
    TWELVE = "12"


class Minutes(Enum):
    ZERO = "0"
    FIFTEEN = "15"
    THIRTY = "30"
    FOURTY_FIVE = "45"


class ReminderCallbackData(CallbackData, prefix="reminder"):
    hour: Hours | None
    minute: Minutes | None


def hours_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for hour in Hours:
        builder.button(
            text=hour.value,
            callback_data=ReminderCallbackData(hour=hour, minute=None),
        )
    builder.button(
        text="⬅️ Назад",
        callback_data=MainMenuActionsCb(action=MainMenuActions.tools).pack(),
    )
    builder.adjust(3)
    return builder.as_markup()


def minutes_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for minute in Minutes:
        builder.button(
            text=minute.value,
            callback_data=ReminderCallbackData(minute=minute, hour=None),
        )
    builder.button(
        text="⬅️ Назад",
        callback_data=ToolsActionsCb(action=ToolsActions.create_event).pack(),
    )
    builder.adjust(2)
    return builder.as_markup()
