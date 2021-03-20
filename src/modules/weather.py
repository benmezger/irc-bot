from typing import Sequence
import asyncio
from aiohttp import ClientSession

from core.plugins import Plugin, register_plugin

URL = "https://wttr.in/{}?format=3"


async def fetch(url: str, session: ClientSession) -> str:
    async with session.get(url) as response:
        return await response.text()


@register_plugin
class Weather(Plugin):
    async def __call__(self, cities: Sequence[str]) -> str:
        cities = list(cities)
        tasks = []
        responses = []

        async with ClientSession() as session:
            for city in cities:
                tasks.append(asyncio.ensure_future(fetch(URL.format(city), session)))

            responses = await asyncio.gather(*tasks)

        for response in responses:
            yield response.strip("\n")
