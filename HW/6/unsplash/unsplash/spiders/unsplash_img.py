import scrapy
from urllib.parse import urljoin


class UnsplashImg(scrapy.Spider):
    name = "unsplash"
    allowed_domains = ["unsplash.com"]
    base = "https://unsplash.com/t/wallpapers"
    short_base = "https://unsplash.com/"

    def parse(self, response, short_base):
        for image_page in response.xpath(".//figure[@itemtype='https://schema.org/ImageObject']/a/@href").extract():
            yield scrapy.Request(response.urljoin(short_base, str(image_page)), self.parse_image_page)

    def parse_image_page(self, response):
        full_url = response.xpath(".//div[@data-test='photos-route']//div/div[1]/div[2]/div/img[2]/@src").extract()
        if full_url:
            yield scrapy.Request(response(full_url), self.save_image)

    def save_image(self, response):
        filename = response.url.split('/'[-1])
        with open (f'images/{filename}', 'wb') as f:
            f.write(response.body)
