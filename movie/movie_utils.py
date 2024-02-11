import requests
import json
from movie.movie_text import movie_types_dict, movie_description
from settings import config
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
import unicodedata


async def get_random_movie(genre_name: str) -> (str, list, list, str):
    """Get random movie from Kinopoisk by genre"""
    try:
        headers = {'X-API-KEY': config.kinopoisk_token}
        url_kinopoisk = f'https://api.kinopoisk.dev/v1.4/movie/random'
        params = {
            'genres.name': genre_name,
            'rating.kp': '6-10',
            'countries.name': ['!Россия',
                               '!Беларусь',
                               '!Индия',
                               '!Азербайджан',
                               '!Таджикистан',
                               '!Узбекистан',
                               '!Украина',
                               '!Иран',
                               '!Египет',
                               '!СССР',
                               '!Казахстан',
                               '!Киргизия',
                               '!Туркменистан',
                               '!Турция'],
            'notNullFields': ['name',
                              'names.name',
                              'description',
                              'shortDescription',
                              'countries.name',
                              'genres.name',
                              'poster.url',
                              'persons.name']
        }
        random_movie = requests.get(url_kinopoisk, params=params, headers=headers)
        trailers = []
        data = json.loads(random_movie.text)
        persons = [person['name'] for person in data['persons']
                   if person['profession'] == 'актеры' and person['name'] is not None]
        if data['poster']['url'] is not None:
            poster = data['poster']['url']
        if 'videos' in data.keys() and len(data['videos']['trailers']) > 0:
            for trailer in data['videos']['trailers']:
                trailers.append([InlineKeyboardButton(text=f'{trailer["name"]}', url=f'{trailer["url"]}')])
        trailers_kb = InlineKeyboardMarkup(inline_keyboard=trailers)
        genres = [genre['name'] for genre in data['genres'] if genre['name'] is not None]
        countries = [country['name'] for country in data['countries'] if country['name'] is not None]
        description = unicodedata.normalize("NFKD", data["description"])
        length = str(data["seriesLength"]) if data['isSeries'] == True else str(data["movieLength"])
        type_ = movie_types_dict[data['type']]
        movie = 'Зацени это😎\n' + movie_description.format(
            name=data["name"],
            countries=", ".join(countries),
            genres=", ".join(genres),
            type=type_,
            description=description,
            persons=", ".join(persons),
            length=length,
            year=data["year"],
            rating=round(data["rating"]["kp"], 1)
        )
        if len(movie) - movie.count('<') - movie.count('>') - movie.count('u') - movie.count('b') - movie.count('/') > 1024:
            short_description = data['shortDescription']
            movie = 'Зацени это😎\n' + movie_description.format(
                name=data["name"],
                countries=", ".join(countries),
                genres=", ".join(genres),
                type=type_,
                description=short_description,
                persons=", ".join(persons),
                length=length,
                year=data["year"],
                rating=round(data["rating"]["kp"], 1)
            )
        return movie, trailers_kb, trailers, poster
    except Exception:
        return None


async def get_movie_description(name: str) -> list | None:
    """Get movie description by name"""
    try:
        headers = {'X-API-KEY': config.kinopoisk_token}
        url_kinopoisk = 'https://api.kinopoisk.dev/v1.3/movie'
        params = {
            'name': name,
            'selectFields': ['name',
                             'description',
                             'shortDescription',
                             'isSeries',
                             'year',
                             'rating',
                             'movieLength',
                             'seriesLength',
                             'genres',
                             'countries',
                             'poster',
                             'videos',
                             'persons',
                             'type'],
            'notNullFields': ['name',
                              'description',
                              'countries.name',
                              'genres.name',
                              'poster.url',
                              'persons.name'],
            'countries.name': ['!Индия',
                               '!Азербайджан',
                               '!Таджикистан',
                               '!Узбекистан',
                               '!Украина',
                               '!Иран',
                               '!Египет'],
            'limit': 5,
            'page': 1
        }
        movies = requests.get(url_kinopoisk, params=params, headers=headers)
        result = []
        data = json.loads(movies.text)
        for film in data['docs']:
            trailers = []
            trailers_kb = ''
            persons = [person['name'] for person in film['persons']
                       if person['profession'] == 'актеры' and person['name'] is not None]
            if film['poster'] is not None:
                poster = types.URLInputFile(film['poster']['url'], filename=f'{film["name"]}.png')
            if 'videos' in film.keys() and len(film['videos']['trailers']) > 0:
                for trailer in film['videos']['trailers']:
                    trailers.append([InlineKeyboardButton(text=f'{film["name"]}', url=f'{trailer["url"]}')])
                trailers_kb = InlineKeyboardMarkup(inline_keyboard=trailers)
            genres = [genre['name'] for genre in film['genres'] if genre['name'] is not None]
            countries = [country['name'] for country in film['countries'] if country['name'] is not None]
            if film["description"] is not None:
                description = unicodedata.normalize("NFKD", film["description"])
            else:
                description = 'Описания, к сожалению, нет'
            length = str(film["seriesLength"]) if film['isSeries'] == True else str(film["movieLength"])
            type_ = movie_types_dict[film['type']] if film['type'] is not None else 'Неизвестно'
            movie = movie_description.format(
                name=film["name"],
                countries=", ".join(countries),
                genres=", ".join(genres),
                type=type_,
                description=description,
                persons=", ".join(persons),
                length=length,
                year=film["year"],
                rating=round(film["rating"]["kp"], 1)
            )
            if len(movie) - movie.count('<') - movie.count('>') - movie.count('u') - movie.count('b') - movie.count('/') > 1024:
                if film["shortDescription"] is not None:
                    short_description = unicodedata.normalize("NFKD", film["shortDescription"])
                else:
                    short_description = 'Описания, к сожалению, нет'
                movie = movie_description.format(
                    name=film["name"],
                    countries=", ".join(countries),
                    genres=", ".join(genres),
                    type=type_,
                    description=short_description,
                    persons=", ".join(persons),
                    length=length,
                    year=film["year"],
                    rating=round(film["rating"]["kp"], 1)
                )
            result.append([movie, trailers, trailers_kb, poster])
        return result
    except Exception:
        return None
