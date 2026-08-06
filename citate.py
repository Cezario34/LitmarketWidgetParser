import requests
from bs4 import BeautifulSoup
url = r'https://litnet.com/ru/reader/reklamnyi-biznes-popadanki-b558729?c=7203696'


response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
author_text = soup.find('div', class_='reader-text font-size-medium').find_all('p')
for author in author_text:
    print(author.get_text())
