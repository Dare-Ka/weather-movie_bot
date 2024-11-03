import asyncio
from datetime import datetime

import aiohttp

from admin.admin import error_notifier
from core.config import settings
from weather.text import weather_dict
from .text import weather_description


async def get_weather_today(
    http_session: aiohttp.ClientSession, city: str
) -> str | None:
    """Get weather description by city name for today"""
    url = settings.weather.url
    headers = {
        "key": settings.weather.token,
    }
    params = {
        "q": city.strip(),
        "days": 1,
        "lang": "ru",
    }
    try:
        async with http_session.get(
            url, params=params, headers=headers
        ) as weather_response:
            if 200 <= weather_response.status < 300:
                data = await weather_response.json()
            else:
                return bot.weather.text.weather_error
    except (aiohttp.ClientError, asyncio.TimeoutError) as error:
        await error_notifier(func_name=get_weather_today.__name__, error=str(error))
        return None

    description = ""
    for time in data["forecast"]["forecastday"][0]["hour"][6:22:3]:
        date = datetime.fromtimestamp(time["time_epoch"]).strftime("%d.%m | %H:%M")
        temp = time["temp_c"]
        feels_like_temp = time["feelslike_c"]
        condition = time["condition"]["text"]
        wind_speed = round(time["wind_kph"] * 1000 / 3600, 1)
        for key, values in weather_dict.items():
            if condition.lower() in values:
                condition += key
        description += weather_description.format(
            date=date,
            temp=temp,
            feels_like_temp=feels_like_temp,
            condition=condition,
            wind_speed=wind_speed,
        )
        if time["will_it_rain"] == 1:
            description += f"Вероятность дождя {time['chance_of_rain']}%\n"
        if time["will_it_snow"] == 1:
            description += f"Вероятность снега {time['chance_of_snow']}%\n"
        description += "\n"
    return f"Вот какая погода сегодня в городе <u>{city}</u>:\n\n" + description
