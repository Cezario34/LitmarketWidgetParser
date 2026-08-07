import requests
from bs4 import BeautifulSoup
from utils import headers


def parse_stats_day_litmarket(base_url) -> dict:
    every_day_pars = {}


    response = requests.get(base_url, headers=headers.headers_pc)
    soup = BeautifulSoup(response.text, 'lxml')
    books_list = soup.find('div', id='booksList')
    books = books_list.find('div', class_='books-list cards-container').find_all('div', class_='item')
    for book in books:
        title = book.find('div', class_='card-title').find('a').get_text()
        author = book.find('div', class_='author').find('a').get_text()
        likes = int(book.find('span', class_='rating-total').get_text())
        libraries = book.find('span', class_='libraries-count').get_text()
        libraries = int(libraries.replace('(', '').replace(')', ''))
        stats = book.find('div', class_='card-statistics')
        if stats:
            icon = stats.find('i', class_='lmfont-views')
            if icon:
                views = icon.parent.get_text(strip=True)
        # =========================================

        every_day_pars[title] = {
            'author': author,
            'library': libraries,
            'likes': likes,
            'views': views  # <-- добавили
            }

    return every_day_pars