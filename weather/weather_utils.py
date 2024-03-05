import requests
import json
from weather.weather_text import weather_dict, weather_description
from datetime import datetime
import os


async def get_weather_today(city: str) -> str | None:
    """Get weather description by city name for today"""
    try:
        weather_today = requests.get(f'https://api.openweathermap.org'
                                     f'/data/2.5/forecast?q={city.strip().lower()}&'
                                     f'lang=ru&cnt=5&appid={os.getenv("API_WEATHER_TOKEN")}&units=metric')
        temp_list = []
        feel_temp_list = []
        time_list = []
        status_list = []
        wind_speed = []
        description = ''
        data = json.loads(weather_today.text)
        for i in range(len(data['list'])):
            temp_list.append(data['list'][i]['main']['temp'])
            feel_temp_list.append(data['list'][i]['main']['feels_like'])
            wind_speed.append(data['list'][i]['wind']['speed'])
            time_list.append(datetime.fromtimestamp(int(data['list'][i]['dt'])).strftime('%d.%m | %H:%M'))
            status_list.append(data['list'][i]['weather'][0]['description'].capitalize())
        for i in range(len(status_list)):
            for key, values in weather_dict.items():
                for value in values:
                    if value.capitalize() == status_list[i]:
                        status_list[i] += key
            description += weather_description.format(
                time=time_list[i],
                temp=round(temp_list[i], 1),
                feel_temp=round(feel_temp_list[i], 1),
                status=status_list[i],
                wind_speed=round(wind_speed[i], 1)
            )
        return f'Вот какая погода сегодня в городе <u>{city}</u>:\n\n' + description
    except Exception:
        return []


async def get_weather_three_days(city: str) -> (str, str, str):
    """Get weather description by city for three days"""
    try:
        weather_today = requests.get(
            f'https://api.openweathermap.org/data/2.5/forecast?q={city.strip().lower()}&lang=ru&&appid={os.getenv("API_WEATHER_TOKEN")}&units=metric')
        temp_list = [[], [], []]
        feel_temp_list = [[], [], []]
        time_list = [[], [], []]
        status_list = [[], [], []]
        wind_speed = [[], [], []]
        description = ['', '', '']
        data = json.loads(weather_today.text)
        for i in range(0, 5):
            temp_list[0].append(data['list'][i]['main']['temp'])
            feel_temp_list[0].append(data['list'][i]['main']['feels_like'])
            wind_speed[0].append(data['list'][i]['wind']['speed'])
            time_list[0].append(datetime.fromtimestamp(int(data['list'][i]['dt'])).strftime('%d.%m | %H:%M'))
            status_list[0].append(data['list'][i]['weather'][0]['description'].capitalize())
        for i in range(len(status_list[0])):
            for key, values in weather_dict.items():
                for value in values:
                    if value.capitalize() == status_list[0][i]:
                        status_list[0][i] += key
            description[0] += weather_description.format(
                time=time_list[0][i],
                temp=round(temp_list[0][i], 1),
                feel_temp=round(feel_temp_list[0][i], 1),
                status=status_list[0][i],
                wind_speed=round(wind_speed[0][i], 1)
            )
        for i in range(5, 10):
            temp_list[1].append(data['list'][i]['main']['temp'])
            feel_temp_list[1].append(data['list'][i]['main']['feels_like'])
            wind_speed[1].append(data['list'][i]['wind']['speed'])
            time_list[1].append(datetime.fromtimestamp(int(data['list'][i]['dt'])).strftime('%d.%m | %H:%M'))
            status_list[1].append(data['list'][i]['weather'][0]['description'].capitalize())
        for i in range(len(status_list[1])):
            for key, values in weather_dict.items():
                for value in values:
                    if value.capitalize() == status_list[1][i]:
                        status_list[1][i] += key
            description[1] += weather_description.format(
                time=time_list[1][i],
                temp=round(temp_list[1][i], 1),
                feel_temp=round(feel_temp_list[1][i], 1),
                status=status_list[1][i],
                wind_speed=round(wind_speed[1][i], 1)
            )
        for i in range(10, 15):
            temp_list[2].append(data['list'][i]['main']['temp'])
            feel_temp_list[2].append(data['list'][i]['main']['feels_like'])
            wind_speed[2].append(data['list'][i]['wind']['speed'])
            time_list[2].append(datetime.fromtimestamp(int(data['list'][i]['dt'])).strftime('%d.%m | %H:%M'))
            status_list[2].append(data['list'][i]['weather'][0]['description'].capitalize())
        for i in range(len(status_list[2])):
            for key, values in weather_dict.items():
                for value in values:
                    if value.capitalize() == status_list[2][i]:
                        status_list[2][i] += key
            description[2] += weather_description.format(
                time=time_list[2][i],
                temp=round(temp_list[2][i], 1),
                feel_temp=round(feel_temp_list[2][i], 1),
                status=status_list[2][i],
                wind_speed=round(wind_speed[2][i], 1)
            )
        day_1 = f'Вот какая погода <u>сегодня</u> в городе <u>{city}</u>:\n\n' + description[0]
        day_2 = f'Вот какая погода <u>завтра</u> в городе {city}:\n\n' + description[1]
        day_3 = f'Вот какая погода <u>послезавтра</u> в городе {city}:\n\n' + description[2]
        return day_1, day_2, day_3
    except Exception:
        return None
