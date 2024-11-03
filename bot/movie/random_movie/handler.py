import asyncio

import aiohttp
from aiogram import Router, F
from aiogram.exceptions import AiogramError
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from admin.admin import error_notifier
from main_menu.keyboard import main_menu_kb_builder
from movie.keyboard import MovieActionsCb, MovieActions
from movie.random_movie.keyboard import (
    show_movie_genres_kb,
    show_movie_types_kb,
    trailers_kb_builder,
    MovieCb,
)
from movie.random_movie.utils import get_random_movie
from movie.text import random_movie_error, movie_types_dict

router = Router(name=__name__)


@router.callback_query(
    MovieActionsCb.filter(F.action == MovieActions.random_movie),
    flags={"chat_action": "typing"},
)
async def ask_type(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.answer()
    await callback.message.edit_text(
        "Что подыскать?", reply_markup=show_movie_types_kb()
    )


@router.callback_query(
    MovieCb.filter(F.type),
    flags={"chat_action": "typing"},
)
async def ask_genre(
    callback: CallbackQuery, callback_data: MovieCb, state: FSMContext
) -> None:
    await callback.answer()
    await state.update_data(movie_type=callback_data.type.value.lower())
    await callback.message.edit_text(
        "В каком жанре?", reply_markup=show_movie_genres_kb()
    )


@router.callback_query(
    MovieCb.filter(F.genre),
    flags={"chat_action": "upload_photo"},
)
async def random_movie(
    callback: CallbackQuery, callback_data: MovieCb, state: FSMContext
) -> None:
    context_data = await state.get_data()
    movie_type = {v.lower(): k for k, v in movie_types_dict.items()}[
        context_data.get("movie_type").lower()
    ]
    genre_name = callback_data.genre.value.lower()
    async with aiohttp.ClientSession() as http_session:
        movie = await get_random_movie(
            http_session, genre_name=genre_name, movie_type=movie_type
        )
    if movie:
        await asyncio.sleep(0.2)
        try:
            await callback.message.delete()
            await callback.message.answer_photo(
                photo=movie[2],
                caption=movie[0],
                parse_mode="HTML",
                reply_markup=trailers_kb_builder(movie[1], as_edit=False),
            )
        except AiogramError as error:
            await asyncio.sleep(0.2)
            await callback.message.edit_text(
                random_movie_error, reply_markup=main_menu_kb_builder()
            )
            await error_notifier(func_name=random_movie.__name__, error=str(error))
    else:
        await asyncio.sleep(0.2)
        await callback.message.edit_text(
            random_movie_error, reply_markup=main_menu_kb_builder()
        )
    await state.clear()
