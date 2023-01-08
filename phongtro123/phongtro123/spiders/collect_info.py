# -*- coding: utf-8 -*-

import scrapy
import json
import re
import datetime

import unidecode

def remove_accent(text):
    if text==None:
        return ""
    return unidecode.unidecode(text)

def listToString(s):
 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        str1 += ele + ' || '
 
    # return string
    return str1

class collect_player_info(scrapy.Spider):
    name='phongtro123_get_info'
  
    def __init__(self):
        try:
            with open('post_url_temp.json') as f:
                self.urls = json.load(f)
                self.url_count = 1
                self.url=''
        except IOError:
            print("File not found")

    def start_requests(self):
        urls = self.urls[0]['link']
        self.url=urls
        yield scrapy.Request(url=urls, callback=self.parse)
  
    def parse(self, response):
        
        info={}        

        
        title=response.xpath('//*[@id="left-col"]/article/header/h1/a/text()').extract_first()
        info['title']=remove_accent(title)
        
        address=response.xpath('//*[@id="left-col"]/article/header/address/text()').extract_first()
        info['address']=remove_accent(address)
        
        price=response.xpath('//*[@id="left-col"]/article/header/div[2]/div[1]/span/text()').extract_first()
        info['price']=remove_accent(price)
        
        acreage=response.xpath('//*[@id="left-col"]/article/header/div[2]/div[2]/span/text()').extract_first()
        info['acreage']=remove_accent(acreage)
        
        
        content=' || '.join(response.css('#left-col > article > section.section.post-main-content > div.section-content p::text').getall())
        info['content']=remove_accent(content)
             
        
        table = response.xpath('//*[@id="left-col"]/article/section[2]/div[2]/table/tr')
        s=remove_accent(table.get())
        
        match=re.search(r'Ma tin:</td><td>#([^<]+)',s)
        if match:
            info['id']=match.group(1)
        else:
            info['id']=None
            
        match=re.search(r'Loai tin rao:</td><td>([^<]+)',s)
        if match:
            info['type_post']=match.group(1)
        else:
            info['type_post']=None
            
        match=re.search(r'Doi tuong thue:</td><td>([^<]+)',s)
        if match:
            info['tenant']=match.group(1)
        else:
            info['tenant']=None
            
        match=re.search(r'Ngay dang:</td><td><time title="([^"]+)">',s)
        if match:
            info['posting_time']=match.group(1)
        else:
            info['posting_time']=None
            
        match=re.search(r'Ngay het han:</td><td><time title="([^"]+)">',s)
        if match:
            info['end_time']=match.group(1)
        else:
            info['end_time']=None
            
        match=re.search(r'Lien he:</td><td> ([^<]+)',s)
        if match:
            info['contact']=match.group(1)
        else:
            info['contact']=None
            
        match=re.search(r'Dien thoai:</td><td> ([^<]+)',s)
        if match:
            info['phone_number']=match.group(1)
        else:
            info['phone_number']=None
            
        match=re.search(r'Zalo</td><td> ([^<]+)',s)
        if match:
            info['zalo']=match.group(1)
        else:
            info['zalo']=None
        
        info['link']=self.url
        #info['type_post']=re.search(r'Loai tin rao:</td><td>([^<]+)',s).group(1)
        #info['tenant']=re.search(r'Doi tuong thue:</td><td>([^<]+)',s).group(1)
        
        #info['posting_time']=re.search(r'Ngay dang:</td><td><time title="([^"]+)">', s).group(1)
        #info['end_time']=re.search(r'Ngay het han:</td><td><time title="([^"]+)">', s).group(1)
        #info['contact']=re.search(r'Lien he:</td><td> ([^<]+)', s).group(1)
        #info['phone_number']=re.search(r'Dien thoai:</td><td> ([^<]+)', s).group(1)     
        #info['zalo']=re.search(r'Zalo</td><td> ([^<]+)', s).group(1)  
        #print(info)
        
        yield info
      
        if self.url_count < len(self.urls):
            next_page_url = self.urls[self.url_count]['link']
            self.url=next_page_url
            self.url_count += 1
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse) 