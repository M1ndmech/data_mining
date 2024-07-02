import requests
from lxml import html
from pymongo import MongoClient
import time

headers_1 = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

# Функция для скрейпинга табличных данных с одной страницы
def scrape_page_data(url, short_url, headers):
    response = requests.get(url, headers)
    tree = html.fromstring(response.content)
    items = tree.xpath("//div[@class='item']")
    data = []
    n = 0
    for item in items:
        try:
            book = tree.xpath(".//div[@class='book']")[n]
            data.append({
                'place': item.xpath(".//h4[@class='index float-left']/text()")[0],
                'title': book.xpath(".//h4/text()")[0],
                'author': book.xpath(".//li[@class='contributor item text-wrap']/a/text()")[0],
                'link': short_url + book.xpath(".//a[@class='title-link d-inline-block']/@href")[0]
                })
            n+=1
        except Exception as ex:
            print (repr(ex))
            print("Last ITEM:", n)
            break
    return data


# Функция для сохранения данных в MongoDB
def save_data_to_mongo(data):
    client = MongoClient('localhost', 27017)
    db = client['scraping']
    collection = db['top100boooks']
    collection.insert_many(data)

# Main function
def main():
    base_url = "https://readrate.com/rus/ratings/top100?iid=8116&offset=all"
    short_url = "https://readrate.com"
    for page in range(1, 1):
        print(f"Scraping page {page}...")
        data = scrape_page_data(base_url, short_url, headers_1)
        save_data_to_mongo(data)
        time.sleep(5)

if __name__ == "__main__":
    main()

