from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from main_menu.keyboard import (
    MainMenuCb,
    MainMenu,
    MainMenuActionsCb,
    MainMenuActions,
)
from movie.keyboard import MovieActionsCb, MovieActions


class MovieTypes(str, Enum):
    film = "Кинофильм"
    tv_series = "TV-сериал"
    movie = "Мультфильм"
    series = "Мультсериал"
    anime = "Аниме"


class MovieGenres(str, Enum):
    comedy = "Комедия"
    drama = "Драма"
    thriller = "Триллер"
    detective = "Детектив"
    fantasy = "Фантастика"


class MovieCb(CallbackData, prefix="movie"):
    type: MovieTypes | None
    genre: MovieGenres | None


def show_movie_types_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for type_ in MovieTypes:
        builder.button(text=type_, callback_data=MovieCb(type=type_, genre=None))
    builder.button(
        text="⬅️ Назад",
        callback_data=MainMenuActionsCb(action=MainMenuActions.movie).pack(),
    )
    builder.adjust(2)
    return builder.as_markup()


def show_movie_genres_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for genre in MovieGenres:
        builder.button(text=genre, callback_data=MovieCb(type=None, genre=genre))
    builder.button(
        text="⬅️ Назад",
        callback_data=MovieActionsCb(action=MovieActions.random_movie).pack(),
    )
    builder.adjust(2)
    return builder.as_markup()


def trailers_kb_builder(
    trailers: InlineKeyboardMarkup, as_edit: bool = True
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.attach(InlineKeyboardBuilder.from_markup(trailers))
    builder.button(
        text=MainMenu.menu.value,
        callback_data=MainMenuCb(main=MainMenu.menu, as_edit=as_edit).pack(),
    )
    builder.adjust(2, 1)
    return builder.as_markup()
