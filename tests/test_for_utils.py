import aiohttp
import os
import pytest

from Crawlers_engine.utils import Utils


@pytest.fixture(scope="module")
async def async_download_page():
    await Utils.download_url("https://ulearn.me")


def test_getting_urls_from_file():
    needed = ["https://yandex.ru/pogoda?from=tableau_yabro&via=hl&lang=ru",
              "https://habr.com/ru/articles/786184"]

    assert needed == Utils.get_urls_from_file(os.getcwd() + "/" + "tested_sites.txt")


@pytest.mark.asyncio
async def test_get_urls_from_site(async_download_page):
    needed = []
    for url in Utils.get_linked_urls(async_download_page, "https://ulearn.me"):
        needed.append(url)
    assert needed == []


@pytest.mark.asyncio
async def test_downloading_page():
    current = await Utils.download_url("https://ulearn/me")
    assert current is None
