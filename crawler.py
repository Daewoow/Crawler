import asyncio
import logging
from bs4 import BeautifulSoup
from task import FetchTask
from typing import Optional
from urllib.parse import urljoin
from utils import Utils

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)


class Crawler:
    def __init__(self, file, depth: int, rtypes: str, ntypes: str, nurls: str,
                 path_to_save: str, maxsize: int, bots: int = 4):
        self.file = file
        self.urls_to_visit = Utils.get_urls_from_file(self.file) if self.file.endswith('txt') else [self.file]
        self.visited_urls = []
        self.max_rate = 3
        self.interval = 5
        self.concurrent_level = 3
        self.is_crawled = False
        self.tasks_queue = asyncio.Queue()
        self._scheduler_task: Optional[asyncio.Task] = None
        self._sem = asyncio.Semaphore(self.max_rate)
        self.concurrent_workers = 0
        self.stop_event = asyncio.Event()
        self.key_words = {}
        self.bots = bots
        self.depth = depth
        self.maxsize = maxsize
        self.path_to_save = path_to_save
        self.rtypes = rtypes.replace(',', '').split()
        self.ntypes = ntypes.replace(',', '').split()
        self.nurls = nurls.replace(',', '').split()

    async def _worker(self, task, tid):
        async with self._sem:
            self.concurrent_workers += 1
            await task.perform(self, tid, self.rtypes, self.ntypes, self.nurls)
            self.tasks_queue.task_done()
        self.concurrent_workers -= 1
        if not self.is_crawled and self.concurrent_workers == 0:
            self.stop_event.set()

    async def stop(self):
        self.is_crawled = False
        self._scheduler_task.cancel()
        if self.concurrent_workers != 0:
            await self.stop_event.wait()

    async def _scheduler(self):
        a = []
        while self.is_crawled:
            for _ in range(self.max_rate):
                task = await self.tasks_queue.get()
                a.append(asyncio.create_task(self._worker(task, task.tid)))
            await asyncio.sleep(self.interval)

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

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    async def crawl(self, url):
        html = await Utils.download_url(url)
        for current_url in self.get_linked_urls(url, html):
            if (current_url and current_url.find('captcha') == -1
                    and not current_url.endswith("rst")
                    and not current_url.startswith("../")):
                self.add_url_to_visit(current_url)

    async def run(self):
        for i in range(1, self.bots):
            await self.tasks_queue.put(FetchTask(tid=i,
                                                 maximum_depth=self.depth,
                                                 path=self.path_to_save,
                                                 maxsize=self.maxsize))
        self.is_crawled = True
        self._scheduler_task = asyncio.create_task(self._scheduler())
        await self.tasks_queue.join()
        await self.stop()
