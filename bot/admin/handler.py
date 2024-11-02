from aiogram import Bot, F, types, Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.fsm.context import FSMContext

from bot.admin.admin import error_notifier
from bot.admin.keyboard import build_admin_kb, AdminActionsCb, AdminActions
from bot.core.config import settings
from bot.core.models import db_helper
from core.schemas.users.crud import get_users, delete_user, get_user, update_user
from core.schemas.users.schemas import UserUpdate
from .state import AdminStates

router = Router()


@router.message(
    F.text.lower() == "админ панель",
    F.from_user.id == settings.bot.admin_id,
    flags={"chat_action": "typing"},
)
async def admin_panel(message: types.Message) -> None:
    await message.answer(
        text="Привет, это панель администратора!",
        reply_markup=build_admin_kb(),
    )


@router.callback_query(
    AdminActionsCb.filter(F.action == AdminActions.mailing),
    F.from_user.id == settings.bot.admin_id,
    flags={"chat_action": "typing"},
)
async def ask_mailing(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(text="Что отправить в рассылке?")
    await state.set_state(AdminStates.mailing_text)


@router.message(
    AdminStates.mailing_text,
    F.from_user.id == settings.bot.admin_id,
)
async def send_mailing(
    message: types.Message,
    state: FSMContext,
    bot: Bot,
) -> None:
    async with db_helper.get_session() as session:
        users = get_users(session=session)

    for user in await users:
        try:
            await message.copy_to(chat_id=user.tg_id)
        except TelegramForbiddenError as error:
            await error_notifier(func_name=send_mailing.__name__, error=error)
            async with db_helper.get_session() as session:
                found_user = await get_user(session=session, tg_id=user.tg_id)
                user_update = UserUpdate(
                    tg_id=user.tg_id,
                    mailing=False,
                    active=False,
                )
                await update_user(
                    session=session, user=found_user, user_update=user_update
                )
            await bot.send_message(
                chat_id=settings.bot.admin_id,
                text=f"Пользователь c id {user.tg_id} деактивирован!",
            )
    await message.answer("Рассылка завершена", reply_markup=build_admin_kb())
    await state.clear()


@router.callback_query(
    AdminActionsCb.filter(F.action == AdminActions.get_users_list),
    F.from_user.id == settings.bot.admin_id,
)
async def get_users_list(callback: types.CallbackQuery) -> None:
    async with db_helper.get_session() as session:
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
    F.from_user.id == settings.bot.admin_id,
)
async def get_user_id(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(text="Введи id пользователя:")
    await state.set_state(AdminStates.user_id)


@router.message(
    AdminStates.user_id,
    F.from_user.id == settings.bot.admin_id,
)
async def get_message(message: types.Message, state: FSMContext) -> None:
    await state.update_data(tg_id=message.text)
    await message.answer(text="Что отправить?")
    await state.set_state(AdminStates.personal_mailing_text)


@router.message(
    AdminStates.personal_mailing_text,
    F.from_user.id == settings.bot.admin_id,
)
async def send_message(message: types.Message, state: FSMContext, bot: Bot) -> None:
    context_data = await state.get_data()
    tg_id = context_data.get("tg_id")
    try:
        await message.copy_to(chat_id=tg_id)
    except TelegramForbiddenError as error:
        await error_notifier(func_name=send_mailing.__name__, error=error)
        async with db_helper.get_session() as session:
            user = await get_user(session=session, tg_id=tg_id)
            found_user = await get_user(session=session, tg_id=user.tg_id)
            user_update = UserUpdate(
                tg_id=user.tg_id,
                mailing=False,
                active=False,
            )
            await update_user(session=session, user=found_user, user_update=user_update)
        await bot.send_message(
            chat_id=settings.bot.admin_id,
            text=f"Пользователь c id {tg_id} деактивирован!",
        )
    await message.answer("Сообщение доставлено!", reply_markup=build_admin_kb())
    await state.clear()


@router.callback_query(
    AdminActionsCb.filter(F.action == AdminActions.delete_user),
    F.from_user.id == settings.bot.admin_id,
)
async def ask_user_id(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(text="Введи tg_id пользователя:")
    await state.set_state(AdminStates.deleting_user_id)


@router.message(
    AdminStates.deleting_user_id,
    F.from_user.id == settings.bot.admin_id,
)
async def delete_user_by_id(message: types.Message, state: FSMContext) -> None:
    tg_id = message.text
    async with db_helper.get_session() as session:
        user = await get_user(session=session, tg_id=tg_id)
        await delete_user(session=session, user=user)
    await message.answer(
        text=f"Пользователь c id {tg_id} удален!",
        reply_markup=build_admin_kb(),
    )
    await state.clear()
