import asyncio
from typing import Tuple, Dict, Union, Any, List
from functools import lru_cache
from aiohttp import ClientSession

from core.plugins import Plugin, register_plugin

URL = "https://cli.fyi/{}"

@lru_cache
async def fetch(
    url: str, session: ClientSession, response_type="json"
) -> Dict[str, Union[Dict[str, str], Dict[str, Dict[str, str]]]]:
    async with session.get(url) as response:
        return await getattr(response, response_type)()


class CliFyiPlugin(Plugin):
    RESPONSE_TYPE = "json"

    def repr(self, data: Dict[Any, Any]):
        raise NotImplemented()

    async def __call__(self, words: Tuple[str]) -> Any:
        words = list(words)
        tasks = []
        responses = []

        async with ClientSession() as session:
            for word in words:
                tasks.append(
                    asyncio.ensure_future(
                        fetch(
                            URL.format(word),
                            session,
                            response_type=self.RESPONSE_TYPE,
                        )
                    )
                )

            responses = await asyncio.gather(*tasks)

        for response in responses:
            yield self.repr(response)


@register_plugin
class IPLookup(CliFyiPlugin):
    RESPONSE_TYPE = "json"

    def repr(self, response: Dict[str, Union[str, Dict[str, str]]]) -> str:
        data = response["data"]

        organisation = data["organisation"]
        country = data["country"]
        country_code = data["countryCode"]

        return f"{organisation}, {country} ({country_code})"


@register_plugin
class WhoIs(CliFyiPlugin):
    RESPONSE_TYPE = "json"

    def repr(self, response: Dict[str, Union[str, Dict[str, str]]]) -> List[str]:
        data = response["data"]
        return [f"| {i} |" for i in data["dns"]]
