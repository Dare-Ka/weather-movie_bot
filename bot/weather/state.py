from aiogram.fsm.state import StatesGroup, State

class Weather(StatesGroup):
    weather_today = State()
    three_days_weather = State()
