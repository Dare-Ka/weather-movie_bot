from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.main_menu.keyboard import (
    MainMenu,
    MainMenuCb,
    MainMenuActionsCb,
    MainMenuActions,
)
from bot.weather.keyboard import WeatherActionCb, WeatherAction, Cities


class WeatherTodayCb(CallbackData, prefix="weather_today"):
    city: Cities


def weather_today_kb_builder() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for city in Cities:
        builder.button(text=city, callback_data=WeatherTodayCb(city=city))
    builder.button(
        text="⬅️ Назад",
        callback_data=MainMenuActionsCb(action=MainMenuActions.weather),
    )
    builder.adjust(2)
    return builder.as_markup()


def weather_today_result_kb_builder(as_edit: bool = True) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Яндекс Погода", url="https://yandex.ru/pogoda/find")
    builder.button(
        text="⬅️ Назад",
        callback_data=WeatherActionCb(action=WeatherAction.weather_today).pack(),
    )
    builder.button(
        text=MainMenu.menu.value,
        callback_data=MainMenuCb(main=MainMenu.menu, as_edit=as_edit).pack(),
    )
    builder.adjust(2, 1)
    return builder.as_markup()
