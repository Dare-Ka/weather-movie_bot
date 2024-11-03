from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from main_menu.keyboard import MainMenuActionsCb, MainMenuActions
from .keyboard import weather_action_kb_builder

router = Router(name=__name__)


@router.callback_query(
    MainMenuActionsCb.filter(F.action == MainMenuActions.weather),
    flags={"chat_action": "typing"},
)
async def handle_choose_weather_action(
    callback: CallbackQuery, state: FSMContext
) -> None:
    await state.clear()
    await callback.answer()
    await callback.message.edit_text(
        text="Выбери действие:", reply_markup=weather_action_kb_builder()
    )
