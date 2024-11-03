from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from main_menu.keyboard import MainMenuCb, MainMenu


class Cities(str, Enum):
    saint_petersburg = "Санкт-Петербург"
    yoshkar_ola = "Йошкар-Ола"
    surgut = "Сургут"
    moscow = "Москва"


class WeatherAction(str, Enum):
    weather_today = "Погода сегодня ⛅️"
    three_days_weather = "Погода на три дня ⛅️"


class WeatherActionCb(CallbackData, prefix="weather"):
    action: WeatherAction


def weather_action_kb_builder() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for action in WeatherAction:
        builder.button(text=action, callback_data=WeatherActionCb(action=action))
    builder.button(text="⬅️ Назад", callback_data=MainMenuCb(main=MainMenu.menu).pack())
    builder.adjust(1)
    return builder.as_markup()
