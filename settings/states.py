from aiogram.fsm.state import StatesGroup, State


class Gen(StatesGroup):
    weather_today = State()
    three_days_weather = State()
    send_message = State()
    movie_description = State()
    genre = State()
    movie_type = State()
    mailing = State()
    personal_mailing = State()
    user_id = State()
    user_id_to_delete = State()


class Scheduler(StatesGroup):
    date = State()
    event = State()


class Settings(StatesGroup):
    mailing = State()
    city = State()
