from aiogram import Bot, F, types, Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.fsm.context import FSMContext

from admin.admin import error_notifier
from admin.keyboard import build_admin_kb, AdminActionsCb, AdminActions
from core.config import settings
from db.models import db
from settings.states import Gen

router = Router()


@router.message(
    F.text.lower() == "админ панель",
    F.from_user.id.in_(settings.ADMIN_ID),
    flags={"chat_action": "typing"},
)
async def admin_panel(message: types.Message, bot: Bot):
    await message.answer(
        text="Привет, это панель администратора!",
        reply_markup=build_admin_kb(),
    )


@router.callback_query(
    AdminActionsCb.filter(F.action == AdminActions.mailing),
    F.from_user.id.in_(settings.ADMIN_ID),
    flags={"chat_action": "typing"},
)
async def ask_mailing(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Что отправить в рассылке?")
    await state.set_state(Gen.mailing)


@router.message(
    Gen.mailing,
    F.from_user.id.in_(settings.ADMIN_ID),
)
async def send_mailing(message: types.Message, state: FSMContext, bot: Bot):
    for tg_id in await db.get_users_info():
        try:
            await message.copy_to(chat_id=tg_id[0])
        except TelegramForbiddenError as error:
            await error_notifier(func_name=send_mailing.__name__, error=error)
            await db.delete_user(tg_id[0])
            await bot.send_message(
                chat_id=settings.ADMIN_ID,
                text=f"Пользователь c id {tg_id[0]} удален!",
            )
    await state.clear()


@router.callback_query(
    AdminActionsCb.filter(F.action == AdminActions.get_users_list),
    F.from_user.id.in_(settings.ADMIN_ID),
)
async def get_users(callback: types.CallbackQuery):
    users = await db.get_users_info()
    users_list = (
        f'У нас {len(users)} пользователей:\n{" | ".join(str(user) for user in users)}'
    )
    if len(users_list) > 4095:
        for message in range(0, len(users_list), 4095):
            await callback.message.answer(text=users_list[message : message + 4095])
    else:
        await callback.message.edit_text(text=users_list, reply_markup=build_admin_kb())


@router.callback_query(
    AdminActionsCb.filter(F.action == AdminActions.send_message),
    F.from_user.id.in_(settings.ADMIN_ID),
)
async def get_user_id(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введи id пользователя:")
    await state.set_state(Gen.user_id)


@router.message(
    Gen.user_id,
    F.from_user.id.in_(settings.ADMIN_ID),
)
async def get_message(message: types.Message, state: FSMContext):
    await state.update_data(tg_id=message.text)
    await message.answer(text="Что отправить?")
    await state.set_state(Gen.personal_mailing)


@router.message(Gen.personal_mailing, F.from_user.id.in_(settings.ADMIN_ID))
async def send_message(message: types.Message, state: FSMContext, bot: Bot):
    context_data = await state.get_data()
    tg_id = context_data.get("tg_id")
    try:
        await message.copy_to(chat_id=tg_id)
    except TelegramForbiddenError as error:
        await error_notifier(func_name=send_mailing.__name__, error=error)
        await db.delete_user(tg_id)
        await bot.send_message(
            chat_id=settings.ADMIN_ID,
            text=f"Пользователь c id {tg_id} удален!",
        )
    await state.clear()


@router.callback_query(
    AdminActionsCb.filter(F.action == AdminActions.delete_user),
    F.from_user.id.in_(settings.ADMIN_ID),
)
async def ask_user_id(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Введи tg_id пользователя:")
    await state.set_state(Gen.user_id_to_delete)


@router.message(Gen.user_id_to_delete, F.from_user.id.in_(settings.ADMIN_ID))
async def delete_user_by_id(message: types.Message, state: FSMContext):
    tg_id = message.text
    await db.delete_user(tg_id)
    await message.answer(
        text=f"Пользователь c id {tg_id} удален!",
        eply_markup=build_admin_kb(),
    )
    await state.clear()
