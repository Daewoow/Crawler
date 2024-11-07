import aiohttp
import os
import re
import requests

from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class Utils:
    @staticmethod
    def save_page(url, maxsize, rtypes, ntypes, nurls, page_path=''):
        session = requests.Session()
        response = session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        path, extension = os.path.splitext(page_path)
        folder = path + '_files'

        for url in nurls:
            if url in folder:
                return

        if rtypes == [] or ntypes == ["All"]:
            return

        if not os.path.exists(folder):
            os.mkdir(folder)
        tags_inner = {
            'img': 'src',
            'link': 'href',
            'script': 'src'
        }

        for tag, inner in tags_inner.items():
            Utils.save_media(soup, folder, session, url, tag, inner, maxsize, rtypes, ntypes, nurls)
            break
        os.chdir(folder)
        with open(path + '.html', 'wb') as file:
            file.write(soup.prettify('utf-8'))
        os.chdir('../')

    @staticmethod
    def save_media(soup, folder, session, url, tag, inner, maxsize, rtypes, ntypes, nurls):
        for resource in soup.findAll(tag):
            if resource.has_attr(inner):
                if (resource[inner].startswith('http') and
                        int(urlopen(resource[inner]).info()['Content-Length']) > maxsize * 1024):
                    continue

                filename, ext = os.path.splitext(os.path.basename(resource[inner]))
                if "all" not in rtypes and ntypes != [""] and ext not in rtypes or ext in ntypes:
                    continue
                filename = re.sub(r'\W+', '', filename) + ext
                file_url = urljoin(url, resource.get(inner))
                filepath = os.path.join(folder, filename)
                resource[inner] = os.path.join(os.path.basename(folder), filename)

                for url in nurls:
                    if url in resource[inner]:
                        continue

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
    def get_linked_urls(url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            if path and path.startswith('mail'):
                continue
            yield path

    @staticmethod
    async def download_url(url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.text()
        except ConnectionRefusedError:
            pass
