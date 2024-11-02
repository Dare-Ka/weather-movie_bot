from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from bot.main_menu.keyboard import (
    MainMenuActions,
    MainMenuActionsCb,
    main_menu_kb_builder,
)
from bot.tools.keyboard import ToolsActionsCb, ToolsActions
from bot.weather.keyboard import Cities


class MailingSettingsActions(str, Enum):
    YES = "да"
    NO = "нет"


class MailingSettingsActionsCb(CallbackData, prefix="mailing_settings"):
    action: MailingSettingsActions | None
    city: Cities | None


def mailing_settings_actions_kb_builder() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for action in MailingSettingsActions:
        builder.button(
            text=action,
            callback_data=MailingSettingsActionsCb(action=action, city=None),
        )
    builder.button(
        text="⬅️ Назад",
        callback_data=MainMenuActionsCb(action=MainMenuActions.tools).pack(),
    )
    builder.adjust(2, 1)
    return builder.as_markup()


def mailing_cities_kb_builder() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for city in Cities:
        builder.button(
            text=city,
            callback_data=MailingSettingsActionsCb(action=None, city=city),
        )
    builder.button(
        text="⬅️ Назад",
        callback_data=ToolsActionsCb(action=ToolsActions.mailing_settings).pack(),
    )
    builder.adjust(2)
    return builder.as_markup()


def retry_mailing_settings() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔄 Попробовать еще",
        callback_data=ToolsActionsCb(action=ToolsActions.mailing_settings),
    )
    builder.attach(InlineKeyboardBuilder.from_markup(main_menu_kb_builder()))
    builder.adjust(1)
    return builder.as_markup()
