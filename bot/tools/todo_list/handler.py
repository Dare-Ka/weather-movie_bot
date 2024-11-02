from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.main_menu.keyboard import main_menu_kb_builder
from bot.tools.keyboard import ToolsActionsCb, ToolsActions

router = Router(name=__name__)


@router.callback_query(ToolsActionsCb.filter(F.action == ToolsActions.todo_list))
async def handle_answer(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        text="В разработке)))", reply_markup=main_menu_kb_builder()
    )
