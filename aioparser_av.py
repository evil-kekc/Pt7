import time
import logging
import certifi
import asyncio
import aiohttp
import ssl
from bs4 import BeautifulSoup


start_time = time.time()

items = []
urls = []
years = []
cashes = []


async def get_page_info(session, page: int):
    global items, urls, years, cashes

    if page == 1:
        url = 'https://cars.av.by/filter?sort=4'
    else:
        url = f'https://cars.av.by/filter?page={page}&sort=4'
    async with session.get(url=url) as response:
        try:
            response_text = await response.text()
            html_source = response_text

            page_info = BeautifulSoup(html_source, 'html.parser')

            car_names = page_info.find_all('a', class_='listing-item__link')
            for name in car_names:
                items.append(name.text)
                urls.append(f"https://cars.av.by{name['href']}")

            items_cashes = page_info.find_all('div', class_='listing-item__priceusd')
            for cash in items_cashes:
                cashes.append(cash.text.replace('&nbsp;', ' '))

            years_html = page_info.find_all('div', class_='listing-item__params')
            for year in years_html:
                for i in year:
                    years.append(i.text)
                    break

        except Exception as e:
            print(f'Error: {repr(e)}')


async def load_site_info():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)

    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = []
        for page in range(1, 51):
            task_1 = asyncio.create_task(get_page_info(session, page))
            tasks.append(task_1)

        await asyncio.gather(*tasks)


async def run_tasks():
    global items, cashes, urls, years
    await load_site_info()
    all_info = list(zip(items, years, cashes, urls))

    for i in all_info:
        print(f'\n\nМарка: {i[0]}, Год: {i[1]}, Цена: {i[2]}, Ссылка: {i[-1]}\n\n')
    print(len(all_info))
    end_time = time.time() - start_time
    print(f'\nВремя работы: {end_time} секунд')


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run_tasks())
    logging.basicConfig(level=logging.DEBUG, filename='my_log.log', datefmt='%H:%M:%S')
