import scrapy

def redLog(msg):
  print('\033[1;31m%s\033[0m'%msg)
class TitleSpider(scrapy.Spider):
  name='title_spider'
  seen=set()
  def start_requests(self):
    yield scrapy.Request(url='https://guba.eastmoney.com/list,zssh000001.html', callback=self.parse)
    for i in range(1,93009):
      url=f'https://guba.eastmoney.com/list,zssh000001_{i}.html'
      yield scrapy.Request(url=url, callback=self.parse)
  def parse(self, response):
    # print(response.text)
    a_arr=response.css('.listitem .title a')
    if len(a_arr)==0:
      redLog('可能出现问题')
    else:
      print(len(a_arr)) 
    pass
  