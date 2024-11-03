import re
import requests
import os
import aiohttp
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class Utils:
    @staticmethod
    def save_page(url, page_path='page'):
        session = requests.Session()
        response = session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        path, extension = os.path.splitext(page_path)
        folder = path + '_files'
        if not os.path.exists(folder):
            os.mkdir(folder)
        tags_inner = {
            'img': 'src',
            'link': 'href',
            'script': 'src'
        }
        for tag, inner in tags_inner.items():
            Utils.save_rename(soup, folder, session, url, tag, inner)
            break
        os.chdir(folder)
        with open(path + '.html', 'wb') as file:
            file.write(soup.prettify('utf-8'))
        os.chdir('../')

    @staticmethod
    def save_rename(soup, folder, session, url, tag, inner):
        for resource in soup.findAll(tag):
            if resource.has_attr(inner):
                filename, ext = os.path.splitext(os.path.basename(resource[inner]))
                filename = re.sub(r'\W+', '', filename) + ext
                file_url = urljoin(url, resource.get(inner))
                filepath = os.path.join(folder, filename)
                resource[inner] = os.path.join(os.path.basename(folder), filename)
                try:
                    if not os.path.isfile(filepath):
                        with open(filepath, 'wb') as file:
                            file_bin = session.get(file_url)
                            file.write(file_bin.content)
                except Exception:
                    pass

    @staticmethod
    def get_urls_from_file(file):
        with open(file) as f:
            urls = re.split(r'\n', f.read())
        return urls

    @staticmethod
    def generate_numbers():
        num = 0
        while True:
            yield num
            num += 1

    @staticmethod
    async def download_url(url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.text()
        except ConnectionRefusedError:
            pass
