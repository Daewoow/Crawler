import asyncclick as click
import asyncio
import logging
from crawler import Crawler

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)


@click.command()
@click.option('--site', required=True, help='URL сайта для сканирования или файл с URL\'ами в формате .txt')
@click.option('--depth', default=2, help='Глубина сканирования (по умолчанию 3).')
@click.option('--path', default="", help='Папка, куда скачивать сайты (по умолчанию - эта)')
@click.option('--maxsize', default=1024, help='Максимальный размер файлов для скачивания в КБ'
                                              ' (по умолчанию - 1024)')
@click.option('--rtypes', default="all", help='Какие типы файлов сохранять (по умолчанию - все)')
@click.option('--ntypes', default="", help='Какие типы файлов не сохранять  (по умолчанию - никакие)')
@click.option('--nurls', default="", help='Какие домены игнорировать при обходе (по умолчанию - никакие) '
                                          'Например: --nurls admin позволит не обходить сайты с admin в названии')
@click.option('--bots', default=4, help="Количество ботов для обхода (по умолчанию - 4)")
async def crawl(site, depth, path, maxsize, rtypes, ntypes, nurls, bots):
    """Краулер"""

    async def run_crawler():
        crawler = Crawler(
            site,
            depth=depth,
            path_to_save=path,
            maxsize=maxsize,
            bots=bots,
            rtypes=rtypes,
            ntypes=ntypes,
            nurls=nurls
        )
        try:
            await crawler.run()
            await asyncio.sleep(.25)
            logging.info("\tThe crawling was ended")
        except Exception as e:
            print(f"An error occurred: {e}")
            await crawler.stop()

    await run_crawler()

if __name__ == '__main__':
    asyncio.run(crawl())
