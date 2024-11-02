from aiogram.fsm.state import StatesGroup, State


class MailingSettings(StatesGroup):
    city = State()
