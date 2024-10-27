import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.chat_action import ChatActionMiddleware

from core.config import settings
from core.middlewares.apschedulermiddleware import SchedulerMiddleware
from core.middlewares.middleware import UserCheckerMiddleware
from core.scheduler.mailing_settings import set_events
from main_menu import router as main_router


async def on_startup(bot: Bot) -> None:
    await bot.send_message(chat_id=settings.MAKSIM_ID, text="Бот запущен!")


async def on_shutdown(bot: Bot) -> None:
    await bot.send_message(chat_id=settings.MAKSIM_ID, text="Бот остановлен!")


async def main():
    bot = Bot(token=settings.TESTS_BOT_TOKEN)
    storage = RedisStorage.from_url("redis://localhost:6379/1")
    scheduler = set_events(bot)
    dp = Dispatcher(storage=storage)
    dp.include_router(main_router)
    dp.message.middleware(ChatActionMiddleware())
    dp.update.middleware.register(UserCheckerMiddleware())
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d %(levelname)s - %(message)s",
    )
    asyncio.run(main())
