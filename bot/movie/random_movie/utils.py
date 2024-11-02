import unicodedata
from pathlib import Path

import aiohttp
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiohttp.web import HTTPNotFound

from bot.admin.admin import error_notifier
from bot.core.config import settings
from bot.movie.text import movie_types_dict, random_movie_description


async def get_random_movie(
    http_session: aiohttp.ClientSession, genre_name: str, movie_type="movie"
) -> (str, list, list, str):
    """Get random movie from Kinopoisk by genre and movie type"""
    headers = {"X-API-KEY": settings.movie.token}
    url_kinopoisk = settings.movie.url + "random"
    params = {
        "genres.name": genre_name,
        "rating.kp": "6-10",
        "countries.name": [
            "!Россия",
            "!Беларусь",
            "!Индия",
            "!Азербайджан",
            "!Таджикистан",
            "!Узбекистан",
            "!Украина",
            "!Иран",
            "!Египет",
            "!СССР",
            "!Казахстан",
            "!Киргизия",
            "!Туркменистан",
            "!Турция",
        ],
        "notNullFields": [
            "name",
            "names.name",
            "description",
            "shortDescription",
            "countries.name",
            "genres.name",
            "poster.url",
            "persons.name",
        ],
        "type": movie_type,
    }
    picture_path = Path(__file__).parent.parent / "movie_pic.jpg"
    print(picture_path)
    try:
        async with http_session.get(
            url_kinopoisk, params=params, headers=headers
        ) as random_movie:
            if 200 <= random_movie.status < 300:
                data = await random_movie.json()
            else:
                return None
    except (HTTPNotFound, TimeoutError) as error:
        await error_notifier(func_name=get_random_movie.__name__, error=str(error))
        return None

    trailers = []
    persons = [
        person["name"]
        for person in data["persons"][0:10]
        if person["profession"] == "актеры" and person["name"] is not None
    ]
    if data["poster"] and data["poster"]["url"]:
        poster = data["poster"]["url"]
    else:
        poster = types.FSInputFile(picture_path)
    if "videos" in data.keys() and len(data["videos"]["trailers"]) > 0:
        for trailer in data["videos"]["trailers"]:
            trailers.append(
                [
                    InlineKeyboardButton(
                        text=f'{trailer["name"]}', url=f'{trailer["url"]}'
                    )
                ]
            )
    trailers_kb = InlineKeyboardMarkup(inline_keyboard=trailers)
    genres = [genre["name"] for genre in data["genres"] if genre["name"] is not None]
    countries = [
        country["name"] for country in data["countries"] if country["name"] is not None
    ]
    description = unicodedata.normalize("NFKD", data["description"])
    length = (
        str(data["seriesLength"])
        if data["isSeries"] == True
        else str(data["movieLength"])
    )
    type_ = movie_types_dict[data["type"]]
    movie = "Зацени это😎\n" + random_movie_description.format(
        name=data["name"],
        countries=", ".join(countries),
        genres=", ".join(genres),
        type=type_,
        description=description,
        persons=", ".join(persons),
        length=length,
        year=data["year"],
        rating=round(data["rating"]["kp"], 1),
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
        short_description = data["shortDescription"]
        movie = "Зацени это😎\n" + random_movie_description.format(
            name=data["name"],
            countries=", ".join(countries),
            genres=", ".join(genres),
            type=type_,
            description=short_description,
            persons=", ".join(persons),
            length=length,
            year=data["year"],
            rating=round(data["rating"]["kp"], 1),
        )
    return movie, trailers_kb, poster
