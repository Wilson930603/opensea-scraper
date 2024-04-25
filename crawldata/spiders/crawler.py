import scrapy,re,requests
from crawldata.functions import *
class CrawlerSpider(scrapy.Spider):
    name = 'opensea_twitter'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8','Accept-Language': 'en-GB,en;q=0.5','Connection': 'keep-alive','Upgrade-Insecure-Requests': '1','Sec-Fetch-Dest': 'document','Sec-Fetch-Mode': 'navigate','Sec-Fetch-Site': 'none','Sec-Fetch-User': '?1',}
    def start_requests(self):
        input_file =re.split('\r\n|\n',open('urls.csv').read())
        for url in input_file:
            if str(url).startswith('https://opensea.io/'):
                yield scrapy.Request('http://httpbin.org/ip',callback=self.parse,meta={'url':url},dont_filter=True)
    def parse(self, response):
        url=response.meta['url']
        HTML=requests.get(url,headers=self.headers)
        response=scrapy.Selector(text=HTML.text)
        TWITTER=response.xpath('//a[contains(@href,"twitter.com")]/@href').get()
        item={}
        item['URL']=url
        item['twitter']=TWITTER
        yield item