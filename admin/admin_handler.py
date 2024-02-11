from settings.states import Gen
from settings import config
from admin.admin_kb import admin_kb, iexit_kb, imenu
from admin.admin_text import menu_text
from admin.admin import error_handler
from db.db import get_users_info, delete_user
import asyncio
from aiogram import Bot, F, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import AiogramError


router = Router()


@router.message(F.text == 'Админ панель', flags={'chat_action': 'typing'})
async def admin_panel(message: types.Message, bot: Bot):
    if message.from_user.id == config.admin_id:
        await message.answer(text='Привет, это панель администратора!', reply_markup=admin_kb)
    else:
        await message.answer(text='Ты не админ!', reply_markup=iexit_kb)
        await bot.send_message(chat_id=config.admin_id,
                               text=f'Нас пытаются взломать!\n'
                                    f'ID: {message.from_user.id}\n'
                                    f'Имя: {message.from_user.first_name}\n'
                                    f'Username: {message.from_user.username}',
                               reply_markup=iexit_kb)


@router.callback_query(F.data == 'mailing')
async def ask_mailing(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введи текст рассылки:')
    await state.set_state(Gen.mailing)


@router.message(Gen.mailing)
async def send_mailing(message: types.Message, state: FSMContext, bot: Bot):
    await state.update_data(text=message.text)
    context_data = await state.get_data()
    text = context_data.get('text')
    for tg_id in await get_users_info():
        try:
            await bot.send_message(chat_id=tg_id[0], text=text)
            await asyncio.sleep(0.1)
        except AiogramError as error:
            await error_handler(str(error), bot)
            await error_handler(error=f'Проблаема с пользователем:\nИмя: {tg_id[1]}\nID: {tg_id[0]}', bot=bot)
            await asyncio.sleep(0.1)
    await bot.send_message(chat_id=config.admin_id, text='Рассылка завершена!', reply_markup=admin_kb)
    await state.clear()


@router.callback_query(F.data == 'get_users_list')
async def get_users(callback: types.CallbackQuery):
    users = await get_users_info()
    users_list = f'У нас {len(users)} пользователей:\n{" | ".join(str(user) for user in users)}'
    if len(users_list) > 4095:
        for message in range(0, len(users_list), 4095):
            await callback.message.answer(text=users_list[message:message+4095])
    else:
        await callback.message.answer(text=users_list,
                                      reply_markup=admin_kb)


@router.callback_query(F.data == 'send_message')
async def get_message(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введи текст сообщения:')
    await state.set_state(Gen.personal_mailing)


@router.message(Gen.personal_mailing)
async def get_user_id(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer(text='Введи id пользователя:')
    await state.set_state(Gen.user_id)


@router.message(Gen.user_id)
async def send_message(message: types.Message, state: FSMContext, bot: Bot):
    await state.update_data(tg_id=message.text)
    context_data = await state.get_data()
    text = context_data.get('text')
    tg_id = context_data.get('tg_id')
    await bot.send_message(chat_id=tg_id, text=text)
    await bot.send_message(chat_id=config.admin_id, text='Сообщение отправлено!', reply_markup=admin_kb)
    await state.clear()


@router.callback_query(F.data == 'back')
async def back(callback: types.CallbackQuery):
    await callback.message.answer(menu_text, reply_markup=imenu)


@router.callback_query(F.data == 'delete_user')
async def ask_user_id(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введи tg_id пользователя:')
    await state.set_state(Gen.user_id_to_delete)


@router.message(Gen.user_id_to_delete)
async def delete_user_by_id(message: types.Message, state: FSMContext):
    await state.update_data(tg_id=message.text)
    context_data = await state.get_data()
    tg_id = context_data.get('tg_id')
    await delete_user(tg_id)
    await message.answer(text='Пользователь удален!', reply_markup=admin_kb)
    await state.clear()
