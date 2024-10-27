from aiogram import Bot, F, types, Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from admin.admin import error_notifier
from admin.keyboard import build_admin_kb, AdminActionsCb, AdminActions
from core.config import settings
from core.models import db_helper
from database.users.crud import get_users, delete_user, get_user
from .state import AdminStates

router = Router()


@router.message(
    F.text.lower() == "админ панель",
    F.from_user.id == settings.ADMIN_ID,
    flags={"chat_action": "typing"},
)
async def admin_panel(message: types.Message):
    await message.answer(
        text="Привет, это панель администратора!",
        reply_markup=build_admin_kb(),
    )


@router.callback_query(
    AdminActionsCb.filter(F.action == AdminActions.mailing),
    F.from_user.id == settings.ADMIN_ID,
    flags={"chat_action": "typing"},
)
async def ask_mailing(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Что отправить в рассылке?")
    await state.set_state(AdminStates.mailing_text)


@router.message(
    AdminStates.mailing_text,
    F.from_user.id == settings.ADMIN_ID,
)
async def send_mailing(
    message: types.Message,
    state: FSMContext,
    bot: Bot,
):
    session: AsyncSession = await db_helper.get_scoped_session()
    users = get_users(session=session)
    for user in await users:
        try:
            await message.copy_to(chat_id=user.tg_id)
        except TelegramForbiddenError as error:
            await error_notifier(func_name=send_mailing.__name__, error=error)
            await delete_user(session=session, user=user)
            await bot.send_message(
                chat_id=settings.ADMIN_ID,
                text=f"Пользователь c id {user.tg_id} удален!",
            )
    await state.clear()


@router.callback_query(
    AdminActionsCb.filter(F.action == AdminActions.get_users_list),
    F.from_user.id == settings.ADMIN_ID,
)
async def get_users_list(callback: types.CallbackQuery):
    session: AsyncSession = await db_helper.get_scoped_session()
    users = await get_users(session=session)
    _ = "\n"
    users_list = (
        f"У нас {len(users)} пользователей:\n"
        f'{" | ".join(f"ID: {user.tg_id}{_}username: @{user.username}{_}Name: {user.tg_name}{_}" for user in users)}'
    )
    if len(users_list) > 4095:
        for message in range(0, len(users_list), 4095):
            await callback.message.answer(text=users_list[message : message + 4095])
    else:
        await callback.message.edit_text(
            text=users_list,
            reply_markup=build_admin_kb(),
        )


@router.callback_query(
    AdminActionsCb.filter(F.action == AdminActions.send_message),
    F.from_user.id == settings.ADMIN_ID,
)
async def get_user_id(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введи id пользователя:")
    await state.set_state(AdminStates.user_id)


@router.message(
    AdminStates.user_id,
    F.from_user.id == settings.ADMIN_ID,
)
async def get_message(message: types.Message, state: FSMContext):
    await state.update_data(tg_id=message.text)
    await message.answer(text="Что отправить?")
    await state.set_state(AdminStates.personal_mailing_text)


@router.message(
    AdminStates.personal_mailing_text, F.from_user.id.in_(settings.ADMIN_ID)
)
async def send_message(message: types.Message, state: FSMContext, bot: Bot):
    context_data = await state.get_data()
    tg_id = context_data.get("tg_id")
    session = await db_helper.get_scoped_session()
    user = await get_user(session=session, tg_id=tg_id)
    try:
        await message.copy_to(chat_id=tg_id)
    except TelegramForbiddenError as error:
        await error_notifier(func_name=send_mailing.__name__, error=error)
        await delete_user(session=session, user=user)
        await bot.send_message(
            chat_id=settings.ADMIN_ID,
            text=f"Пользователь c id {tg_id} удален!",
        )
    await state.clear()


@router.callback_query(
    AdminActionsCb.filter(F.action == AdminActions.delete_user),
    F.from_user.id == settings.ADMIN_ID,
)
async def ask_user_id(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Введи tg_id пользователя:")
    await state.set_state(AdminStates.user_id)


@router.message(
    AdminStates.user_id,
    F.from_user.id == settings.ADMIN_ID,
)
async def delete_user_by_id(message: types.Message, state: FSMContext):
    tg_id = message.text
    session = await db_helper.get_scoped_session()
    user = await get_user(session=session, tg_id=tg_id)
    await delete_user(session=session, user=user)
    await message.answer(
        text=f"Пользователь c id {tg_id} удален!",
        reply_markup=build_admin_kb(),
    )
    await state.clear()
