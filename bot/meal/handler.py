import asyncio

from aiogram import types, F, Router

from bot.main_menu.keyboard import MainMenuActionsCb, MainMenuActions
from bot.meal.keyboard import meal_kb_builder
from bot.meal.utils import get_random_meal

router = Router(name=__name__)


@router.callback_query(
    MainMenuActionsCb.filter(F.action == MainMenuActions.meal),
    flags={"chat_action": "typing"},
)
async def random_meal(callback: types.CallbackQuery) -> None:
    meal = await get_random_meal()
    await asyncio.sleep(0.2)
    await callback.message.edit_text(
        text=meal, parse_mode="HTML", reply_markup=meal_kb_builder()
    )
