import asyncio

from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from .keyboard import main_menu_actions_kb_builder, MainMenuCb
from .text import menu_text, hello

router = Router(name=__name__)


@router.message(Command("start"), flags={"chat_action": "typing"})
async def start(message: Message) -> None:
    await asyncio.sleep(0.2)
    await message.answer(
        hello.format(name=message.from_user.first_name),
        reply_markup=main_menu_actions_kb_builder(),
    )


@router.message(F.text.lower() == "меню")
async def menu(message: Message) -> None:
    await message.delete()
    await message.answer(menu_text, reply_markup=main_menu_actions_kb_builder())


@router.callback_query(
    MainMenuCb.filter(F.as_edit == False),
    flags={"chat_action": "typing"},
)
async def show_main_menu(
    callback: types.CallbackQuery, callback_data: MainMenuCb, state: FSMContext
) -> None:
    await state.clear()
    await callback.message.answer(
        callback_data.main.value, reply_markup=main_menu_actions_kb_builder()
    )


@router.callback_query(
    MainMenuCb.filter(F.as_edit == True),
    flags={"chat_action": "typing"},
)
async def show_main_menu_with_edit(
    callback: types.CallbackQuery, callback_data: MainMenuCb, state: FSMContext
):
    await state.clear()
    await callback.message.edit_text(
        callback_data.main.value, reply_markup=main_menu_actions_kb_builder()
    )
