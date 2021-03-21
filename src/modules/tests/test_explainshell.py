import pytest
import aiohttp
from aioresponses import aioresponses, CallbackResult

from modules.explainshell import ExplainShell, fetch, URL


async def test_fetch():
    session = aiohttp.ClientSession()
    with aioresponses() as m:
        m.get(
            URL,
            callback=lambda *args, **kwargs: CallbackResult(
                status=200, body="ls(1)\n list directory contents"
            ),
        )

        response = await fetch(URL, session)
        assert response == "ls(1)\n list directory contents"


async def test_explainshell(mocker):
    mocked_fetch = mocker.patch(
        "modules.explainshell.fetch", return_value="Hello, world\nI am returning..."
    )

    [_ async for _ in ExplainShell(shellcmd=("ls",))][0] == [
        "Hello, world",
        "I am returning",
    ]

    assert mocked_fetch.call_count == 1
    assert mocked_fetch.call_args[0][0] == "https://www.mankier.com/api/explain/?q=ls"
