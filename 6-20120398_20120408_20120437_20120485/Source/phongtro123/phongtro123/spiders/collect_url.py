import scrapy
import re

class Phongtro123Spider(scrapy.Spider):
    name = 'phongtro123_get_url'
    start_urls = ['https://phongtro123.com/tinh-thanh/ho-chi-minh?page=1']
    
    def __init__(self):
        self.page_count = 1
        self.end_page =0

    def parse(self, response):
        for item in response.css('div.post-meta'):
            link=item.css('a::attr(href)').get()
            if link!=None:
                yield {
                    'link':'https://phongtro123.com'+ link
                }
            #print(link)
        
        if self.page_count == 1:
            end_page = response.css('#left-col > ul > li:nth-child(6) > a').attrib['href']
            end_page=int(re.findall('[0-9]+',end_page)[-1])
            self.end_page=end_page
        
        self.page_count=self.page_count+1
        if self.page_count<=self.end_page:
            next_page='https://phongtro123.com/tinh-thanh/ho-chi-minh?page='+ str(self.page_count)
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
            
        print('Number of page:'+str(end_page))
