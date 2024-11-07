import asyncio
import os
import pytest
import shutil
from Crawler.Crawlers_engine.crawler import Crawler


def remove_folders_by_names(directory, folder_names):
    for folder_name in folder_names:
        folder_path = directory + "/" + folder_name[2:]
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)


@pytest.mark.asyncio
async def test_nurls():
    bad_name = "habr"
    test_crawler = Crawler("tested_sites.txt", 2,
                           "all", "", bad_name, "", 1024)

    await test_crawler.run()
    await asyncio.sleep(.25)

    assertion_result = True

    folders = []
    for entry in os.scandir("./"):
        if entry.is_dir():
            folders.append(entry.path)

    for folder in folders:
        if "cache" in folder:
            folders.remove(folder)
            continue
        if bad_name in folder:
            assertion_result = False

    remove_folders_by_names(os.getcwd(), folders)

    assert assertion_result


@pytest.mark.asyncio
async def test_bad_types():
    test_crawler = Crawler("tested_sites.txt", 2,
                           "", "", "", "", 1024)

    await test_crawler.run()
    await asyncio.sleep(.25)

    assertion_result = True

    folders = []
    for entry in os.scandir("./"):
        if entry.is_dir():
            folders.append(entry.path)

    for folder in folders:
        if "cache" in folder:
            folders.remove(folder)
            continue
        assertion_result = False

    remove_folders_by_names(os.getcwd(), folders)

    assert assertion_result


@pytest.mark.asyncio
async def test_bad_size():
    test_crawler = Crawler("tested_sites.txt", 2,
                           "", "", "", "", 0)

    await test_crawler.run()
    await asyncio.sleep(.25)

    assertion_result = True

    folders = []
    for entry in os.scandir("./"):
        if entry.is_dir():
            folders.append(entry.path)

    for folder in folders:
        if "cache" in folder:
            folders.remove(folder)
            continue
        assertion_result = False

    remove_folders_by_names(os.getcwd(), folders)

    assert assertion_result

