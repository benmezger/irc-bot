from typing import Sequence
import asyncio
from aiohttp import ClientSession

from core.plugins import Plugin, register_plugin

URL = "https://www.mankier.com/api/explain/?q={}"


async def fetch(url: str, session: ClientSession) -> str:
    async with session.get(url) as response:
        return await response.text()


@register_plugin(
    name="explain", description="explain shell command", arguments="ls -al"
)
class ExplainShell(Plugin):
    async def __call__(self, shellcmd: Sequence[str]) -> str:
        cmd = " ".join(shellcmd)

        async with ClientSession() as session:
            response = await fetch(URL.format(cmd), session)

        yield [_.strip() for _ in response.split("\n") if _ != ""]
