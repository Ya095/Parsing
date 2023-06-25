#------------------------------------------------
# Парсинг страниц drom.ru и запись в excel файл
#------------------------------------------------

import requests
from bs4 import BeautifulSoup
import csv


CSV = 'data/parsing.csv'
HOST = 'https://auto.drom.ru/'
URL = 'https://auto.drom.ru/mercedes-benz/all/'
HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


# Получаем контент одной конкретной страницы 
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='css-xb5nz8 ewrty961')
    cards = []

    # Получаем нужный контент из элемента
    for item in items:
        cards.append(
            {
                'title': item.find('span', {'data-ftid': 'bull_title'}).get_text(),
                'link_product': item.get('href'),
                'price': item.find('span', {'data-ftid': 'bull_price'}).get_text().replace('\xa0', '')
            }
        )
    return cards


# Сохранение данных в файл excel
def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['title', 'link', 'price']) # первая строка - заголовки

        # Записываем строки
        for item in items:
            writer.writerow([item['title'], item['link_product'], item['price']])


# Парсинг
def parsing():
    try:
        PAGINATION = int(input('Укажите количество страниц для парсинга: ').strip())
        html = get_html(URL)
        if html.status_code == 200:
            cards = []

            # Работа со страницами
            for page in range(1, PAGINATION+1):
                print(f'Парсим страницу {page}')
                html = get_html(URL, params={'page': page})
                cards.extend(get_content(html.text))
                save_doc(cards, CSV)
        else:
            print('Error. Status code != 200')
    except ValueError:
        print("Введите число")


parsing()