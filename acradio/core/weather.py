import asyncio
from enum import StrEnum
import python_weather
from python_weather.enums import Kind

class Weather(StrEnum):
    SUNNY = "sunny"
    RAINY = "rainy"
    SNOWY = "snowy"

async def _get_weather(place: str) -> Weather:
    client = python_weather.Client()
    forecast = await client.get(place)

    match forecast.kind:
        case Kind.SUNNY | Kind.PARTLY_CLOUDY | Kind.CLOUDY | Kind.VERY_CLOUDY | Kind.FOG:
            return Weather.SUNNY
        case Kind.LIGHT_SHOWERS | Kind.THUNDERY_SHOWERS | Kind.LIGHT_RAIN | Kind.HEAVY_SHOWERS | Kind.HEAVY_RAIN | Kind.THUNDERY_HEAVY_RAIN:
            return Weather.RAINY
        case Kind.LIGHT_SLEET_SHOWERS | Kind.LIGHT_SLEET | Kind.LIGHT_SNOW | Kind.HEAVY_SNOW | Kind.LIGHT_SNOW_SHOWERS | Kind.HEAVY_SNOW_SHOWERS | Kind.THUNDERY_SNOW_SHOWERS:
            return Weather.SNOWY
        case _:
            return Weather.SUNNY

def get_weather(place: str) -> Weather:
    return asyncio.run(_get_weather(place))
