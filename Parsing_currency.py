#-------------------------------------
# Парсер курс $ США с сайта минфина.
#-------------------------------------

import requests
from bs4 import BeautifulSoup
import re


def get_usa_dollar_value():
    url = 'https://www.cbr.ru/currency_base/daily/'

    source = requests.get(url)
    main_text = source.text
    soup = BeautifulSoup(main_text, "html.parser")
    table = soup.find('table', {'class' : 'data'})

    usa_dollar_value = re.search(r"Доллар США+\n+(\d|,){7}", table.text).group()
    return usa_dollar_value

print(get_usa_dollar_value())