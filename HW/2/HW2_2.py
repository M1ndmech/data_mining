import requests
import json
import re
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}
url = 'https://books.toscrape.com/catalogue/'

def paginator(url, headers):
    page_n = 0
    data = []
    while True:
        try:
            page_n+=1
            page = url + f'page-{page_n}.html'
            data += page_scraper(url, page, headers)
        except Exception as ex:
            print (repr(ex))
            print("Last page:", page)
            break
    with open('books_data.json', 'a') as file:
        json.dump(data, file, indent = 4)

def page_scraper(url, page, headers):
    response = requests.get(page, headers=headers)
    if response.status_code == 200:
        page_soup = BeautifulSoup(response.content, 'html.parser')
        books = page_soup.find_all('article', class_='product_pod')
        books_data = []
        for book in books:
            title = book.h3.a['title']
            price = float(book.find('p', class_ = 'price_color').get_text()[1:])
            description_url = url + book.h3.a['href']
            description_response = requests.get(description_url)
            description_soup = BeautifulSoup(description_response.content, 'html.parser')
            description = description_soup.find_all('p', string=True)[1].text
            stock = re.findall("[0-9]+", str(description_soup.find_all('p', class_='instock availability')))[0]
            results = ({
                'title': title,
                'price': price,
                'stock': int(stock),
                'description': description
                })
            books_data.append(results)
        return (books_data)
        
paginator(url, headers)
