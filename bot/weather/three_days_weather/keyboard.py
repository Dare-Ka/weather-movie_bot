from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from main_menu.keyboard import (
    MainMenu,
    MainMenuCb,
    MainMenuActionsCb,
    MainMenuActions,
)
from weather.keyboard import WeatherActionCb, WeatherAction, Cities


class WeatherThreeDaysCb(CallbackData, prefix="weather_three_days"):
    city: Cities


def weather_three_days_kb_builder() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for city in Cities:
        builder.button(text=city, callback_data=WeatherThreeDaysCb(city=city))
    builder.button(
        text="⬅️ Назад",
        callback_data=MainMenuActionsCb(action=MainMenuActions.weather).pack(),
    )
    builder.adjust(2)
    return builder.as_markup()


def three_days_weather_result_kb_builder(as_edit: bool = True) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Яндекс Погода", url="https://yandex.ru/pogoda/find")
    builder.button(
        text="⬅️ Назад",
        callback_data=WeatherActionCb(action=WeatherAction.three_days_weather).pack(),
    )
    builder.button(
        text=MainMenu.menu.value,
        callback_data=MainMenuCb(main=MainMenu.menu, as_edit=as_edit).pack(),
    )
    builder.adjust(2, 1)
    return builder.as_markup()
