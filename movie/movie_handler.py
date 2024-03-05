from admin.admin import error_handler
from movie.movie_utils import get_random_movie, get_movie_description
from movie.movie_text import random_movie_error, movie_error
from movie.movie_kb import random_movie_back, movie_genres
from settings.states import Gen
from handlers.handlers_kb import menu_kb, iexit_kb
from db.db import update_user
import asyncio
from aiogram import types, F, Bot, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

router = Router()


@router.callback_query(F.data == 'get_random_movie', flags={'chat_action': 'typing'})
async def ask_genre(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.username:
        await update_user(tg_id=callback.from_user.id,
                          tg_name=callback.from_user.first_name,
                          username='@' + callback.from_user.username
                          )
    else:
        await update_user(tg_id=callback.from_user.id,
                          tg_name=callback.from_user.first_name,
                          username='Скрыто'
                          )
    await asyncio.sleep(0.2)
    await callback.message.answer('Привет, рад тебя видеть! В каком жанре подобрать тебе фильм?',
                                  reply_markup=movie_genres)
    await state.set_state(Gen.random_movie)


@router.message(Gen.random_movie, flags={'chat_action': 'upload_photo'})
async def random_movie(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(genre=message.text.lower())
    context_data = await state.get_data()
    genre = context_data.get('genre')
    res = await get_random_movie(genre_name=genre)
    try:
        if res is None:
            await state.clear()
            await asyncio.sleep(0.2)
            await message.answer(random_movie_error, reply_markup=random_movie_back)
        await asyncio.sleep(0.2)
        await message.answer_photo(photo=res[3],
                                   caption=res[0],
                                   parse_mode="HTML",
                                   reply_markup=menu_kb
                                   )
        if len(res[2]) != 0:
            await message.answer('Не понял описание? Посмотри трейлер🔥', reply_markup=res[1])
            await state.clear()
        else:
            await message.answer('Трейлера, к сожалению, нет', reply_markup=iexit_kb)
            await state.clear()
    except Exception as error:
        await error_handler('get_random_movie:\n' + str(error), bot)
        await state.clear()


@router.callback_query(F.data == 'movie_description', flags={'chat_action': 'typing'})
async def ask_name(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.username:
        await update_user(tg_id=callback.from_user.id,
                          tg_name=callback.from_user.first_name,
                          username='@' + callback.from_user.username
                          )
    else:
        await update_user(tg_id=callback.from_user.id,
                          tg_name=callback.from_user.first_name,
                          username='Скрыто'
                          )
    await asyncio.sleep(0.2)
    await callback.message.answer("Привет, рад тебя видеть! Какой фильм интересует?😉")
    await state.set_state(Gen.movie_description)


@router.message(Gen.movie_description, flags={'chat_action': 'upload_photo'})
async def movie_description(message: types.Message, state: FSMContext, bot: Bot):
    await state.update_data(name=message.text)
    context_data = await state.get_data()
    name = context_data.get('name')
    movies = await get_movie_description(name)
    if len(movies) == 0:
        await asyncio.sleep(0.2)
        await message.answer(movie_error, reply_markup=iexit_kb)
    for description in movies:
        try:
            await asyncio.sleep(0.3)
            await message.answer_photo(photo=description[-1],
                                       caption=description[0],
                                       parse_mode="HTML",
                                       reply_markup=menu_kb
                                       )
            if len(description[1]) != 0:
                await message.answer('Не понял описание? Посмотри трейлер🔥', reply_markup=description[2])
            else:
                await message.answer('Трейлера, к сожалению, нет', reply_markup=iexit_kb)
        except Exception as error:
            await error_handler('get_movie_description:\n' + str(error), bot)
    await state.clear()
