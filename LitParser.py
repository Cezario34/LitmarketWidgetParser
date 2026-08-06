import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_stats_day(url) -> dict:
    base_url = r'https://litnet.com/'
    every_day_pars = {}

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    books = soup.find_all('div', class_='row book-item')
    for book in books:
        print(book)
        book_info = book.find('div', class_='col-xs-7')
        title = book_info.find('h4',class_='book-title').find('a')
        book_title = title.get_text().strip()
        link = title.get('href')
        full_link = urljoin(base_url, link)
        library_and_views = book_info.find('div', class_='pull-left')
        library = int(library_and_views.find('span', class_='count-views').get_text())
        views = int(library_and_views.find('span', class_='count-favourites').get_text())
        every_day_pars[book_title] = {'full_link': full_link, 'library': library, 'views': views}

    return every_day_pars
