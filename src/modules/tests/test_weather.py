import pytest
import aiohttp
from aioresponses import aioresponses, CallbackResult

from modules.weather import Weather, fetch, URL


async def test_fetch():
    session = aiohttp.ClientSession()
    with aioresponses() as m:
        m.get(
            URL,
            callback=lambda *args, **kwargs: CallbackResult(
                status=200, body="Amsterdam: -1"
            ),
        )

        response = await fetch(URL, session)
        assert response == "Amsterdam: -1"


async def test_weather(mocker):
    mocked_fetch = mocker.patch(
        "modules.weather.fetch", side_effect=("Amsterdam: -1", "Paris: -1")
    )

    assert [
        _
        async for _ in Weather(
            cities=(
                "Amsterdam",
                "Paris",
            )
        )
    ] == ["Amsterdam: -1", "Paris: -1"]
    assert mocked_fetch.call_count == 2
    assert mocked_fetch.call_args_list[0][0][0] == "https://wttr.in/Amsterdam?format=3"
    assert mocked_fetch.call_args_list[1][0][0] == "https://wttr.in/Paris?format=3"
