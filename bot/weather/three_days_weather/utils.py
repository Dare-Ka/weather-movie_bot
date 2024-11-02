import asyncio
from datetime import datetime

import aiohttp
from aiohttp.web_exceptions import HTTPNotFound

from bot.admin.admin import error_notifier
from bot.core.config import settings
from bot.weather.text import weather_dict, weather_error
from .text import weather_description


async def get_weather_three_days(http_session: aiohttp.ClientSession, city: str) -> str:
    """Get weather description by city for three days"""
    url = settings.weather.url
    headers = {
        "key": settings.weather.token,
    }
    params = {
        "q": city.strip(),
        "days": 3,
        "lang": "ru",
    }
    try:
        async with http_session.get(
            url,
            params=params,
            headers=headers,
        ) as weather_response:
            if 200 <= weather_response.status < 300:
                data = await weather_response.json()
            else:
                return weather_error
    except (HTTPNotFound, asyncio.TimeoutError) as error:
        await error_notifier(
            func_name=get_weather_three_days.__name__, error=str(error)
        )
        return None

    description = ""
    for day in data["forecast"]["forecastday"]:
        date = datetime.fromtimestamp(day["date_epoch"]).strftime("%d.%m.%Y")
        max_temp = day["day"]["maxtemp_c"]
        min_temp = day["day"]["mintemp_c"]
        condition = day["day"]["condition"]["text"]
        wind_speed = round(day["day"]["maxwind_kph"] * 1000 / 3600, 1)
        for key, values in weather_dict.items():
            if condition.lower() in values:
                condition += key
        description += weather_description.format(
            date=date,
            max_temp=max_temp,
            min_temp=min_temp,
            condition=condition,
            wind_speed=wind_speed,
        )
        if day["day"]["daily_will_it_rain"] == 1:
            description += f"Вероятность дождя {day['day']['daily_chance_of_rain']}%\n"
        if day["day"]["daily_will_it_snow"] == 1:
            description += f"Вероятность снега {day['day']['daily_chance_of_snow']}%\n"
        description += "\n"
    return description
