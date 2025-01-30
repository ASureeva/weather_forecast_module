import math
import random
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.weather import WeatherData
import requests

wind_directions = {0: 'N', 10: 'N', 20: 'N', 30: 'NE', 40: 'NE', 50: 'NE', 60:  'NE',
                   70: 'E', 80: 'E', 90: 'E', 100: 'E', 110: 'E', 120: 'SE', 130: 'SE',
                   140: 'SE', 150: 'SE', 160: 'S', 170: 'S', 180: 'S', 190: 'S',
                   200: 'S', 210: 'SW', 220: 'SW', 230: 'SW', 240: 'SW', 250: 'W',
                   260: 'W', 270: 'W', 280: 'W', 290: 'W', 300: 'NW', 310: 'NW',
                   320: 'NW', 330: "NW", 340: 'N', 350: 'N', 360: 'N'}


async def get_current_weather():
    lat = '55.760029'
    lon = '49.180399'
    appid = '13a9abef360f89b873f661a48bc0cd67'
    URL = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={appid}'
    r = requests.get(URL)
    info = r.json()
    wind_speed = info['wind']['speed']
    wind_direction = info['wind']['deg']
    precipitation_type = 'none'
    precipitation_intensity = 0.0
    if 'snow' in info.keys():
        precipitation_type = 'snow'
        precipitation_type = float(info['snow']['1h'])
    elif 'rain' in info.keys():
        precipitation_type = 'rain'
        precipitation_type = float(info['rain']['1h'])

    record = {
        'wind_speed': wind_speed,
        'wind_direction': wind_directions[wind_direction],
        'precipitation_type': precipitation_type,
        'precipitation_intensity': precipitation_intensity
    }

    return record
