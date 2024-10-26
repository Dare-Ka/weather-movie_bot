import asyncio

import aiohttp
from aiogram import types, F, Router
from aiogram.exceptions import AiogramError
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from admin.errors import error_notifier
from main_menu.keyboard import main_menu_kb_builder
from movie.find_movie_by_name.keyboard import (
    find_movie_by_name_result_kb_builder,
    find_movie_actions_kb_builder,
)
from movie.find_movie_by_name.utils import get_movie_description
from movie.keyboard import MovieActionsCb, MovieActions
from movie.state import Movie
from movie.text import movie_error

router = Router(name=__name__)


@router.callback_query(
    MovieActionsCb.filter(F.action == MovieActions.find_movie_by_name),
    flags={"chat_action": "typing"},
)
async def ask_name(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(
        "Какой фильм интересует?😉", reply_markup=find_movie_actions_kb_builder()
    )
    await state.set_state(Movie.movie_name)


@router.message(
    Movie.movie_name,
    flags={"chat_action": "upload_photo"},
)
async def movie_description(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    context_data = await state.get_data()
    name = context_data.get("name")
    async with aiohttp.ClientSession() as http_session:
        movies = await get_movie_description(http_session, name)
    if movies:
        for description in movies:
            try:
                await asyncio.sleep(0.3)
                await message.answer_photo(
                    photo=description[1],
                    caption=description[0],
                    parse_mode="HTML",
                    reply_markup=find_movie_by_name_result_kb_builder(
                        description[2], as_edit=False
                    ),
                )
            except AiogramError as error:
                await error_notifier(
                    func_name=movie_description.__name__, error=str(error)
                )
    else:
        await asyncio.sleep(0.2)
        await message.answer(
            movie_error, reply_markup=main_menu_kb_builder(as_edit=False)
        )
    await state.clear()
