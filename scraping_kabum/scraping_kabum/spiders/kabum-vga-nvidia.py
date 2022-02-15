import json

import scrapy
import numpy as np
import pandas as pd
from re import escape


class KabumVgaNvidia(scrapy.Spider):
    name = 'crawler_kabum_nvidia_vga'
    base_url = 'https://www.kabum.com.br'

    @staticmethod
    def generate_urls(page_number=1):
        return f'https://www.kabum.com.br/hardware/placa-de-video-vga?page_number={page_number}&page_size=20'

    start_urls = [generate_urls()]

    def parse(self, response):
        last_page_number = int(response.xpath('//*[@id="listingPagination"]/ul/li')[-2].xpath('a/text()').extract_first())
        for i in range(last_page_number):
            print(i)
            yield scrapy.Request(self.generate_urls(i), self.parse_cards)


    def parse_cards(self, response):
        cards = response.xpath('//main[contains(class, productCard)]')[1].xpath('div')
        get_link = np.vectorize(lambda e: e.xpath("a/@href").extract_first())

        gpus=[]
        for card in cards:
            link = f'{KabumVgaNvidia.base_url}{card.xpath("a/@href").extract_first()}'
            gpu_image = escape(card.xpath('a/img/@src').extract_first())
            gpu_name = card.xpath("a/div/div[1]/h2/text()").extract_first()

            price = escape(card.xpath("a/div/div[2]/span[2]/text()").extract_first().replace(u'\xa0', u' '))
            #print(price)
            gpus.append({'gpu_name': gpu_name, 'price': price, 'image_src': gpu_image, 'link': link})

        list_gpu_cards = np.array(cards)

        with open(f'placas-nvidia.json', 'a', encoding='utf-8') as f:
            json.dump(gpus, f, ensure_ascii=False)
            self.log(f'Saved file')

