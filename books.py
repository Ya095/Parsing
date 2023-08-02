import json
import time
import requests
import datetime
import csv
from bs4 import BeautifulSoup
import asyncio
import aiohttp


# задача; сбор и сохранение инф. со страницы
async def get_page_data(session, page):
    pass


# формирование списка задач
async def gather_data():
    HEADERS = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    URL = "https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table"

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=URL, headers=HEADERS)
        soup = BeautifulSoup(await response.text(), 'lxml')
        pages_count = int(soup.find("div", class_="pagination-numbers").find_all("a")[-1].text)

        tasks = []
        for page in range(1, pages_count+1):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)

def main():
    pass


if __name__ == '__main__':
    main()