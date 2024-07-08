import scrapy
from pymongo import MongoClient

class DnsLaptopsSpider(scrapy.Spider):
    name = "dns_shop"
    allowed_domains = ["dns-shop.ru"]
    start_urls = ["https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/"]

    def parse(self, response):
        for page in response.xpath(".//a[@class='catalog-product__name ui-link ui-link_black']/@href").extract():
            yield scrapy.Request(response.urljoin(page), callback=self.parse_page)

    def parse_page(self, response):
        name = response.xpath(".//div[@class='product-card-top__name']/text()").extract_first().strip()
        price = response.xpath(".//div[@class='product-buy__price']/text()").extract_first().strip()
        specs = {}
        for item in response.xpath(".//div[@class='product-characteristics__spec product-characteristics__ovh']"):
            spec = item.xpath(".//div/text()").extract_first().strip()
            spec_data = item.xpath(".//a/text()").extract_first().strip()
            specs[spec] = spec_data
        product = {
            'name': name,
            'price': price,
            'specs': specs
        }
        yield product
        self.save_to_mongo(product)

    def save_to_mongo(self, item):
        client = MongoClient('mongodb://localhost:27017/')
        db = client['scraping']
        collection = db['laptops']
        collection.insert_one(item)

 