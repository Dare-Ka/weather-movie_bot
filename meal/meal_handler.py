from meal.meal_utils import get_random_meal
from meal.meal_text import dinner_again, hmm
from meal.meal_kb import meal_back
from db.db import update_user
import asyncio
from random import choice
from aiogram import types, F, Router

router = Router()


@router.callback_query(F.data == 'random_meal', flags={'chat_action': 'typing'})
async def random_meal(callback: types.CallbackQuery):
    if callback.from_user.username:
        await update_user(tg_id=callback.from_user.id,
                          tg_name=callback.from_user.first_name,
                          username='@' + callback.from_user.username
                          )
    else:
        await update_user(tg_id=callback.from_user.id,
                          tg_name=callback.from_user.first_name,
                          username='Скрыто'
                          )
    res = await get_random_meal()
    await asyncio.sleep(0.2)
    await callback.message.answer_sticker(sticker=choice(hmm))
    await asyncio.sleep(1.5)
    await callback.message.answer(res, parse_mode="HTML")
    await callback.message.answer(text=dinner_again, reply_markup=meal_back)
