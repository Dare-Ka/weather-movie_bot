from admin.admin import error_handler
from movie.movie_utils import get_random_movie, get_movie_description
from movie.movie_text import random_movie_error, movie_error, movie_types_dict
from movie.movie_kb import random_movie_back, movie_genres, movie_types_kb
from settings.states import Gen
from handlers.handlers_kb import menu_kb, iexit_kb
import asyncio
from aiogram import types, F, Bot, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

router = Router()


@router.callback_query(F.data == 'get_random_movie', flags={'chat_action': 'typing'})
async def ask_type(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Что подыскать?',
                                  reply_markup=movie_types_kb)
    await state.set_state(Gen.movie_type)


@router.message(Gen.movie_type, flags={'chat_action': 'typing'})
async def ask_genre(message: Message, state: FSMContext):
    await state.update_data(movie_type=message.text.lower())
    await asyncio.sleep(0.2)
    await message.answer('В каком жанре?',
                         reply_markup=movie_genres)
    await state.set_state(Gen.genre)


@router.message(Gen.genre, flags={'chat_action': 'upload_photo'})
async def random_movie(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(genre=message.text.lower())
    context_data = await state.get_data()
    genre = context_data.get('genre')
    movie_type = {v.lower(): k for k, v in movie_types_dict.items()}[context_data.get('movie_type').lower()]
    res = await get_random_movie(genre_name=genre, movie_type=movie_type)
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
    await callback.message.edit_text("Какой фильм интересует?😉")
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
            await message.answer_photo(photo=description[1],
                                       caption=description[0],
                                       parse_mode="HTML",
                                       reply_markup=description[2]
                                       )
        except Exception as error:
            await error_handler('get_movie_description:\n' + str(error), bot)
    await state.clear()
