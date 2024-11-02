import unicodedata
from pathlib import Path

import aiohttp
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiohttp.web import HTTPNotFound

from bot.admin.admin import error_notifier
from bot.core.config import settings
from bot.movie.text import movie_types_dict, movie_description


async def get_movie_description(
    http_session: aiohttp.ClientSession, name: str
) -> list[str, types.URLInputFile, InlineKeyboardMarkup] | None:
    """Get movie description by name"""
    headers = {"X-API-KEY": settings.movie.token}
    url_kinopoisk = settings.movie.url + "search"
    params = {
        "query": name,
        "limit": 2,
        "page": 1,
    }
    picture_path = Path(__file__).parent.parent / "movie_pic.jpg"
    try:
        async with http_session.get(
            url_kinopoisk, params=params, headers=headers
        ) as movies:
            if 200 <= movies.status < 300:
                data = await movies.json()
            else:
                return None
    except (HTTPNotFound, TimeoutError) as error:
        await error_notifier(func_name=get_movie_description.__name__, error=str(error))
        return None

    result = []

    for film in data["docs"]:
        link = []
        if film["isSeries"] == True:
            link.append(
                [
                    InlineKeyboardButton(
                        text="КиноПоиск",
                        url=f'https://www.kinopoisk.ru/series/{film["id"]}/',
                    )
                ]
            )
        else:
            link.append(
                [
                    InlineKeyboardButton(
                        text="КиноПоиск",
                        url=f'https://www.kinopoisk.ru/film/{film["id"]}/',
                    )
                ]
            )
        link_kb = InlineKeyboardMarkup(inline_keyboard=link)
        if film["poster"] and film["poster"]["url"]:
            poster = types.URLInputFile(
                film["poster"]["url"], filename=f'{film["name"]}.png'
            )
        else:
            poster = types.FSInputFile(picture_path)
        genres = [
            genre["name"] for genre in film["genres"] if genre["name"] is not None
        ]
        countries = [
            country["name"]
            for country in film["countries"]
            if country["name"] is not None
        ]
        if film["description"] is not None:
            description = unicodedata.normalize("NFKD", film["description"])
        else:
            description = "Описания, к сожалению, нет"
        length = (
            str(film["seriesLength"])
            if film["isSeries"] == True
            else str(film["movieLength"])
        )
        type_ = (
            movie_types_dict[film["type"]] if film["type"] is not None else "Неизвестно"
        )
        movie = movie_description.format(
            name=film["name"],
            countries=", ".join(countries),
            genres=", ".join(genres),
            type=type_,
            description=description,
            length=length,
            year=film["year"],
            rating=round(film["rating"]["kp"], 1),
        )
        if (
            len(movie)
            - movie.count("<")
            - movie.count(">")
            - movie.count("u")
            - movie.count("b")
            - movie.count("/")
            > 1024
        ):
            if film["shortDescription"] is not None:
                short_description = unicodedata.normalize(
                    "NFKD", film["shortDescription"]
                )
            else:
                short_description = "Описания, к сожалению, нет"
            movie = movie_description.format(
                name=film["name"],
                countries=", ".join(countries),
                genres=", ".join(genres),
                type=type_,
                description=short_description,
                length=length,
                year=film["year"],
                rating=round(film["rating"]["kp"], 1),
            )
        result.append([movie, poster, link_kb])
    return result
