from aiogram.fsm.state import StatesGroup, State


class Reminder(StatesGroup):
    hour = State()
    minute = State()
    event = State()
