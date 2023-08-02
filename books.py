import json
import datetime
import csv
from bs4 import BeautifulSoup
import asyncio
import aiohttp


books_data = []
URL = "https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table"
HEADERS = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }


# задача; сбор и сохранение инф. со страницы
async def get_page_data(session, page):

    page_url = f"https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table&page={page}"

    async with session.get(url=page_url, headers=HEADERS) as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, 'html.parser')
        books_items = soup.find("tbody", class_="products-table__body").find_all("tr")

        for bi in books_items:
            book_data = bi.find_all("td")

            try:
                book_title = book_data[0].find("a").text.strip()
                if book_title == '':
                    continue
            except Exception:
                book_title = "Нет названия книги"

            try:
                book_author = book_data[1].text.strip()
            except Exception:
                book_author = "Нет автора"

            try:
                book_publishing = book_data[2].find_all("a")
                book_publishing = ":".join([bp.text for bp in book_publishing])
            except Exception:
                book_publishing = "Нет издательства"

            try:
                book_new_price = int(
                    book_data[3].find("div", class_="price").find("span").find("span").text.strip().replace(" ", ""))
            except Exception:
                book_new_price = "Нет нового прайса"

            try:
                book_old_price = int(book_data[3].find("span", class_="price-gray").text.strip().replace(" ", ""))
            except Exception:
                book_old_price = "Нет старого прайса"

            try:
                book_sale = round(((book_old_price - book_new_price) / book_old_price) * 100)
            except Exception:
                book_sale = "Нет скидки"

            try:
                book_status = book_data[-1].text.strip()
            except Exception:
                book_status = "Нет статуса"

            books_data.append(
                {
                    "book_title": book_title,
                    "book_author": book_author,
                    "book_publishing": book_publishing,
                    "book_new_price": book_new_price,
                    "book_old_price": book_old_price,
                    "book_sale": book_sale,
                    "book_status": book_status
                }
            )

        print(f'Закончен парсинг страницы {page}')


# формирование списка задач
async def gather_data():

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=URL, headers=HEADERS)
        soup = BeautifulSoup(await response.text(), 'html.parser')
        pages_count = int(soup.find("div", class_="pagination-numbers").find_all("a")[-1].text)

        tasks = []

        for page in range(1, pages_count + 1):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    asyncio.get_event_loop().run_until_complete(gather_data())

    cur_time = datetime.datetime.now().date()
    with open(f"labirint_{cur_time}.json", "w") as file:
        json.dump(books_data, file, indent=4, ensure_ascii=False)

    with open(f"labirint_{cur_time}.csv", "w") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Название книги",
                "Автор",
                "Издательство",
                "Цена со скидкой",
                "Цена без скидки",
                "Процент скидки",
                "Наличие на складе"
            )
        )

    for book in books_data:
        with open(f"labirint_{cur_time}.csv", "a") as file:
            writer = csv.writer(file)

            writer.writerow(
                (
                    book["book_title"],
                    book["book_author"],
                    book["book_publishing"],
                    book["book_new_price"],
                    book["book_old_price"],
                    book["book_sale"],
                    book["book_status"]
                )
            )


if __name__ == '__main__':
    main()