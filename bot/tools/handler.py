from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from main_menu.keyboard import MainMenuActionsCb, MainMenuActions
from tools.keyboard import tools_kb_builder

router = Router(name=__name__)


@router.callback_query(
    MainMenuActionsCb.filter(F.action == MainMenuActions.tools),
    flags={"chat_action": "typing"},
)
async def choose_tool_action(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.answer()
    await callback.message.edit_text(
        "Выбери действие:",
        reply_markup=tools_kb_builder(),
    )
