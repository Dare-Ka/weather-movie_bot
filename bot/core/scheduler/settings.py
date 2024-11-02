from datetime import datetime

from aiogram import Bot
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator

from bot.core.scheduler import scheduled_events


def set_events(bot: Bot) -> ContextSchedulerDecorator:
    """Sets up events for scheduler"""
    jobstores = {
        "default": RedisJobStore(
            jobs_key="dispatched_trips_job",
            run_times_key="dispatched_trips_running",
            host="localhost",
            port=6379,
            db=2,
        )
    }
    scheduler = ContextSchedulerDecorator(
        AsyncIOScheduler(timezone="Europe/Moscow", jobstores=jobstores)
    )
    scheduler.ctx.add_instance(bot, declared_class=Bot)
    scheduler.start()
    if not scheduler.get_job("good_night"):
        scheduler.add_job(
            scheduled_events.good_night,
            trigger="cron",
            hour="21",
            minute="00",
            start_date=datetime.now(),
            id="good_night",
        )
    if not scheduler.get_job("good_morning"):
        scheduler.add_job(
            scheduled_events.good_morning,
            trigger="cron",
            day_of_week="0-4",
            hour="08",
            minute="00",
            start_date=datetime.now(),
            id="good_morning",
        )
    if not scheduler.get_job("good_vacation"):
        scheduler.add_job(
            scheduled_events.good_vacation,
            trigger="cron",
            day_of_week="5-6",
            hour="09",
            minute="00",
            start_date=datetime.now(),
            id="good_vacation",
        )
    if not scheduler.get_job("movie_mailing"):
        scheduler.add_job(
            scheduled_events.movie_mailing,
            trigger="cron",
            hour="18",
            minute="00",
            start_date=datetime.now(),
            id="movie_mailing",
        )
    if not scheduler.get_job("happy_ny"):
        scheduler.add_job(
            scheduled_events.happy_ny,
            trigger="cron",
            month="04",
            day="31",
            hour="23",
            minute="59",
            start_date=datetime.now(),
            id="happy_ny",
        )
    return scheduler
