from movie.movie_text import movie_types_dict, movie_description, random_movie_description
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
import unicodedata
import logging
import aiohttp
import config


async def get_random_movie(genre_name: str, movie_type='movie') -> (str, list, list, str):
    """Get random movie from Kinopoisk by genre and movie type"""
    http_session = aiohttp.ClientSession()
    try:
        for token in config.API_KINOPOISK_TOKEN_LIST:
            headers = {'X-API-KEY': token}
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
                                  'persons.name'],
                'type': movie_type
            }
            random_movie = await http_session.get(url_kinopoisk, params=params, headers=headers)
            if random_movie.status == 200:
                break
            else:
                continue
        trailers = []
        data = await random_movie.json()
        persons = [person['name'] for person in data['persons']
                   if person['profession'] == 'актеры' and person['name'] is not None]
        if data['poster'] and data['poster']['url']:
            poster = data['poster']['url']
        else:
            poster = types.FSInputFile(r'/my_bots/Harper/movie/movie_pic.jpg')
        if 'videos' in data.keys() and len(data['videos']['trailers']) > 0:
            for trailer in data['videos']['trailers']:
                trailers.append([InlineKeyboardButton(text=f'{trailer["name"]}', url=f'{trailer["url"]}')])
        trailers_kb = InlineKeyboardMarkup(inline_keyboard=trailers)
        genres = [genre['name'] for genre in data['genres'] if genre['name'] is not None]
        countries = [country['name'] for country in data['countries'] if country['name'] is not None]
        description = unicodedata.normalize("NFKD", data["description"])
        length = str(data["seriesLength"]) if data['isSeries'] == True else str(data["movieLength"])
        type_ = movie_types_dict[data['type']]
        movie = 'Зацени это😎\n' + random_movie_description.format(
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
            movie = 'Зацени это😎\n' + random_movie_description(
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
        await http_session.close()
        return movie, trailers_kb, trailers, poster
    except Exception as e:
        logging.error(e)
        return None


async def get_movie_description(name: str) -> list | None:
    """Get movie description by name"""
    http_session = aiohttp.ClientSession()
    try:
        for token in config.API_KINOPOISK_TOKEN_LIST:
            headers = {'X-API-KEY': token}
            url_kinopoisk = 'https://api.kinopoisk.dev/v1.4/movie/search'
            params = {
                'query': name,
                'limit': 5,
                'page': 1
            }
            movies = await http_session.get(url_kinopoisk, params=params, headers=headers)
            if movies.status == 200:
                break
            else:
                continue
        result = []
        data = await movies.json()
        for film in data['docs']:
            link = []
            if film['isSeries'] == True:
                link.append([InlineKeyboardButton(text='КиноПоиск',
                                                  url=f'https://www.kinopoisk.ru/series/{film["id"]}/')])
            else:
                link.append([InlineKeyboardButton(text='КиноПоиск',
                                                  url=f'https://www.kinopoisk.ru/film/{film["id"]}/')])
            link_kb = InlineKeyboardMarkup(inline_keyboard=link)
            if film['poster'] and film['poster']['url']:
                poster = types.URLInputFile(film['poster']['url'], filename=f'{film["name"]}.png')
            else:
                poster = types.FSInputFile(r'/my_bots/Harper/movie/movie_pic.jpg')
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
                length=length,
                year=film["year"],
                rating=round(film["rating"]["kp"], 1)
            )
            if len(movie) - movie.count('<') - movie.count('>') - movie.count('u') - movie.count('b') - movie.count(
                    '/') > 1024:
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
                    length=length,
                    year=film["year"],
                    rating=round(film["rating"]["kp"], 1)
                )
            result.append([movie, poster, link_kb])
        await http_session.close()
        return result
    except Exception as e:
        logging.error(e)
        return []

