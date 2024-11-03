# import asyncio
# from errors import FileFormatError
# from crawler import Crawler
#
#
# if __name__ == '__main__':
#     def get_text_file():
#         try:
#             path = input()
#             if not path.endswith('.txt'):
#                 raise FileFormatError('File must be ended by .txt')
#             return path
#         except FileFormatError as e:
#             print(str(e))
#             path = get_text_file()
#             return path
#
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#
#     # file = get_text_file()
#     crawler = Crawler('sites.txt', depth=2)
#     try:
#         asyncio.run(crawler.run())
#     except Exception:
#         asyncio.run(crawler.stop())
#         loop.stop()
