import config
import events.events_handler
import handlers.handlers
import meal.meal_handler
import movie.movie_handler
import settings.settings_handler
import weather.weather_handler
import admin.admin_handler
from db.models import db, backup_db
from middleware.throttlingmiddleware import ThrottlingMessageMiddleware, ThrottlingCallBackMiddleware
from events.events import good_night, good_morning, happy_ny, donate, good_vacation, movie_mailing
from middleware.apschedulermiddleware import SchedulerMiddleware
import asyncio
import logging
import datetime
from aiogram import Bot, Dispatcher
from aiogram.utils.chat_action import ChatActionMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler_di import ContextSchedulerDecorator


async def start_bot(bot: Bot):
    await bot.send_message(chat_id=config.ADMIN_ID, text='Бот запущен!')
    await db.create_table()
    await backup_db.create_table()


async def stop_bot(bot: Bot):
    await bot.send_message(chat_id=config.ADMIN_ID, text='Бот остановлен!')


async def main():
    bot = Bot(token=config.TESTBOT_TOKEN)
    storage = RedisStorage.from_url('redis://localhost:6379/0')
    message_throttling_storage = RedisStorage.from_url('redis://localhost:6379/1')
    callback_throttling_storage = RedisStorage.from_url('redis://localhost:6379/3')
    dp = Dispatcher(storage=storage)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    jobstores = {
        'default': RedisJobStore(jobs_key='dispatched_trips_job',
                                 run_times_key='dispatched_trips_running',
                                 host='localhost',
                                 port=6379,
                                 db=2)
    }
    dp.message.middleware.register(ThrottlingMessageMiddleware(storage=message_throttling_storage))
    dp.callback_query.middleware.register(ThrottlingCallBackMiddleware(storage=callback_throttling_storage))
    dp.include_router(handlers.handlers.router)
    dp.include_router(events.events_handler.router)
    dp.include_router(meal.meal_handler.router)
    dp.include_router(movie.movie_handler.router)
    dp.include_router(weather.weather_handler.router)
    dp.include_router(admin.admin_handler.router)
    dp.include_router(settings.settings_handler.router)
    scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone='Europe/Moscow', jobstores=jobstores))
    scheduler.ctx.add_instance(bot, declared_class=Bot)
    dp.message.middleware(ChatActionMiddleware())
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    scheduler.start()
    if not scheduler.get_job('good_night'):
        scheduler.add_job(good_night,
                          trigger='cron',
                          hour='21',
                          minute='00',
                          start_date=datetime.datetime.now(),
                          id='good_night')
    if not scheduler.get_job('good_morning'):
        scheduler.add_job(good_morning,
                          trigger='cron',
                          day_of_week='0-4',
                          hour='08',
                          minute='00',
                          start_date=datetime.datetime.now(),
                          id='good_morning')
    if not scheduler.get_job('good_vacation'):
        scheduler.add_job(good_vacation,
                          trigger='cron',
                          day_of_week='5-6',
                          hour='09',
                          minute='00',
                          start_date=datetime.datetime.now(),
                          id='good_vacation')
    if not scheduler.get_job('movie_mailing'):
        scheduler.add_job(movie_mailing,
                          trigger='cron',
                          hour='18',
                          minute='00',
                          start_date=datetime.datetime.now(),
                          id='movie_mailing')
    if not scheduler.get_job('happy_ny'):
        scheduler.add_job(happy_ny,
                          trigger='cron',
                          month='04',
                          day='31',
                          hour='23',
                          minute='59',
                          start_date=datetime.datetime.now(),
                          id='happy_ny')
    if not scheduler.get_job('donate'):
        scheduler.add_job(donate,
                          trigger='cron',
                          day='3rd thu',
                          hour='17',
                          minute='00',
                          start_date=datetime.datetime.now(),
                          id='donate')
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
