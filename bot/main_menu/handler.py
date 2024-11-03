import asyncio

from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.admin.admin import new_user_event
from bot.core.models import db_helper
from core.schemas.users.crud import add_user, get_user, update_user
from core.schemas.users.schemas import UserCreate, UserUpdate
from .keyboard import main_menu_actions_kb_builder, MainMenuCb
from .text import menu_text, hello

router = Router(name=__name__)


@router.message(Command("start"), flags={"chat_action": "typing"})
async def start(
    message: Message,
) -> None:
    await asyncio.sleep(0.2)
    async with db_helper.get_session() as session:
        found_user = await get_user(session=session, tg_id=message.from_user.id)
        if found_user:
            user_update = UserUpdate(
                tg_id=message.from_user.id,
                active=True,
            )
            await update_user(session=session, user=found_user, user_update=user_update)
        else:
            user = UserCreate(
                tg_id=message.from_user.id,
                tg_name=message.from_user.first_name,
                username=message.from_user.username,
            )
            await new_user_event(await add_user(session=session, user_in=user))
    await message.answer(
        hello.format(name=message.from_user.first_name),
        reply_markup=main_menu_actions_kb_builder(),
    )


@router.message(
    F.text.lower() == "меню",
    flags={"chat_action": "typing"},
)
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
    await callback.answer()
    await state.clear()
    await callback.message.answer(
        callback_data.main.value,
        reply_markup=main_menu_actions_kb_builder(),
    )


@router.callback_query(
    MainMenuCb.filter(F.as_edit == True),
    flags={"chat_action": "typing"},
)
async def show_main_menu_with_edit(
    callback: types.CallbackQuery, callback_data: MainMenuCb, state: FSMContext
) -> None:
    await callback.answer()
    await state.clear()
    await callback.message.edit_text(
        callback_data.main.value,
        reply_markup=main_menu_actions_kb_builder(),
    )
