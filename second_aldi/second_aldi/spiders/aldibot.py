
import scrapy


class AldibotSpider(scrapy.Spider):
    name = 'aldibot'
    allowed_domains = ['aldi.com.au']
    start_urls = ['https://www.aldi.com.au/en/special-buys/easter/',
                  'https://www.aldi.com.au/en/groceries/super-savers/']

    def parse(self, response):
            for per_page_url in response.css('.tab-nav--list.dropdown--list.ym-clearfix a::attr("href")').extract():
                top_level_category=per_page_url.split("/")[-3]
                subcategory=per_page_url.split("/")[-2]
                yield response.follow(per_page_url, callback=self.parse_per_page,meta={'top_level_category': top_level_category,'subcategory':subcategory})


   
    def parse_per_page(self, response):
       #Extract product information
       top_level_category=response.meta.get('top_level_category')
       subcategory=response.meta.get('subcategory')
       product_name=response.css(".box--description--header::text").extract() 
       image_url= response.xpath('//div[@class="box m-text-image"]/div/div/img/@src').extract() 
       product_url= response.css(".box--wrapper.ym-gl.ym-g25::attr(href)").extract()
       price=response.css(".box--value::text,.box--decimal::text").extract() 
       price=[ ''.join(x) for x in zip(price[0::2], price[1::2]) ]


       for item in zip(product_name,image_url,product_url,price):
           scraped_info = {
              'top_level_category':top_level_category,
              'subcategory':subcategory,
              'product_name' : item[0].strip(),
              'image_url' : item[1],
              'product_url' : item[2],
              'price' : item[3],
              
           }

           yield scraped_info

