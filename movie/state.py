from aiogram.fsm.state import StatesGroup, State


class Movie(StatesGroup):
    movie_name = State()
    genre = State()
    movie_type = State()
