from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    mailing_text = State()
    user_id = State()
    deleting_user_id = State()
    personal_mailing_text = State()
