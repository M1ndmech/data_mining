import requests
import json
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

url = 'https://books.toscrape.com'

page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.text, 'html.parser')

def books_scraper(url, page, soup):
    categories = soup.find('div', class_='side_categories').find_all('a')
    category_links = [url + category['href'] for category in categories]
    books_data = []

    for category_link in category_links:
        response = requests.get(category_link)
        if response.status_code == 200:
            category_soup = BeautifulSoup(response.content, 'html.parser')
            books = category_soup.find_all('article', class_='product_pod')
            for book in books:
                title = book.h3.a['title']
                price = float(book.find('p', class_ = 'price_color').get_text()[1:])
                stock = int(book.find('p', class_='instock availability').contents[2].strip().split()[1])
                
            



    with open('books_data.json', 'w') as file:
        json.dump(books_data, file, indent = 4)