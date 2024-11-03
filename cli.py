import asyncclick as click
import asyncio
import logging
from crawler import Crawler

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

@click.command()
@click.option('--site', required=True, help='URL сайта для сканирования.')
@click.option('--depth', default=3, help='Глубина сканирования (по умолчанию 3).')
@click.option('--timeout', default=10, help='Таймаут запроса в секундах (по умолчанию 10).')
@click.option('--output', default='output.txt', help='Файл для сохранения результатов (по умолчанию output.txt).')
async def crawl(site, depth, timeout, output):
    """Асинхронный инструмент для сканирования веб-сайтов."""

    async def run_crawler():
        crawler = Crawler(site, depth=depth)
        try:
            await crawler.run()
            await asyncio.sleep(.25)

        except Exception as e:
            print(f"An error occurred: {e}")
            await crawler.stop()

    await run_crawler()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(crawl())
