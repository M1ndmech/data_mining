import scrapy
from pymongo import MongoClient

class DnsLaptopsSpider(scrapy.Spider):
    name = "dns_shop"
    allowed_domains = ["www.dns-shop.ru"]
    start_urls = ["https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/"]

    def parse(self, response):
        for page in response.xpath(".//a[@class='catalog-product__name ui-link ui-link_black']/@href").extract():
            yield scrapy.Request(response.urljoin(response, page), self.parse_page)

    def parse_page(self, response):
        name = item.xpath(".//div[@class='product-card-top__name']/text()").extract()
        price = item.xpath(".//div[@class='product-buy__price']/text()").extract()
        specs = {}
        for item in response.xpath(".//div[class='product-characteristics__spec product-characteristics__ovh']").extract():
            spec = item.xpath(".//div/text()").extract()
            spec_data = item.xpath(".//a/text()").extract()
            specs += {spec: spec_data}
        yield ({
                'name': name,
                'price': price,
                'specs': specs
            })
    
    def save_to_mongo(self, response):
        client = MongoClient('mongodb://localhost:27017/')
        db = client['scraping']
        collection = db['laptops']
        collection.insert_many(response.body)
