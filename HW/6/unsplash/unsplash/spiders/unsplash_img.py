import scrapy
from urllib.parse import urljoin

import scrapy.resolver

class UnsplashImg(scrapy.Spider):
    name = "unsplash"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/t/wallpapers"]
    count = 0

    def parse(self, response):
        for image_page in response.xpath(".//figure[@itemtype='https://schema.org/ImageObject']/a/@href").extract():
            yield scrapy.Request(urljoin("https://unsplash.com/", image_page), self.parse_image_page)

    def parse_image_page(self, response):
        full_url = response.xpath(".//div[@data-test='photos-route']//div/div[1]/div[2]/div/img[2]/@src").get()
        if full_url:
            yield scrapy.Request(full_url, self.save_image)

    def save_image(self, response):
        name = response.url.split('/')[-1]
        name = name.split('?fm=jpg')
        name = name[:1]
        name = ' '.join(name)
        with open (f'images\\{name}.jpg','wb') as f:
            f.write(response.body)