import re
import time
import urllib
from urllib.error import HTTPError
import urllib.request
from bs4 import BeautifulSoup
import logging
from peewee import *
import random
import concurrent.futures

class Book:
  def __init__(self, title, author='',desc='',score='', price='',real_price='', publisher='',publish_time='', tag=''):
    self.title = title
    self.author = author
    self.desc = desc
    self.score = score
    self.price = price
    self.real_price = real_price
    self.publisher = publisher
    self.tag = tag
    self.publish_time=publish_time
    
# 连接到数据库
db = SqliteDatabase('douban/sqlite.db')
class BOOKS(Model):
      title = CharField()
      author = CharField()
      desc = TextField()
      score = CharField()
      price = CharField()
      real_price = CharField()
      publisher = CharField()
      tag = CharField()
      publish_time = DateField(formats='%Y-%m')
      class Meta:
          database = db  # 指定数据库
# 创建表
db.connect()
db.create_tables([BOOKS])


def tag_spider(tag,start,end):
  "[start,end)"
  page=start*20
  repeat=0
  ua_list=[  
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16'
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
]
  while True:
    time.sleep(random.randint(2, 4))
    try:
      url = 'https://book.douban.com/tag/'+urllib.parse.quote(tag)+f'?start={page}&type=T'
      headers = {
          'User-Agent':ua_list[page//20%len(ua_list)],
      }
      repeat+=1
      request = urllib.request.Request(url, headers=headers)
      with urllib.request.urlopen(request) as f:
        html_doc = f.read().decode('utf-8')
      soup = BeautifulSoup(html_doc,'lxml')
      subject_list=soup.find_all('li',class_='subject-item')
      if not subject_list or len(subject_list)==0:
        break
      books=[]
      for li in subject_list:
        title=li.find('h2').find('a').get_text().replace('\n', '').replace(' ', '').strip()
        desc=''
        score=''
        real_price=''
        price=''
        publishTime=''
        publisher=''
        author=''
        if desc_ele:=li.find('p'):
          desc=desc_ele.get_text().strip()
        if score_ele:=li.find('span', class_='rating_nums'):
          score=score_ele.get_text().strip()
        if real_price_ele:=li.find('span', class_='buy-info'):
          real_price_str=real_price_ele.get_text().strip()
          match=re.search(r'\d+\.\d+|\d+', real_price_str)
          if match:
            real_price=match.group()
        if pub_ele:=li.find('div', class_='pub'):
          if info_:=pub_ele.get_text().strip():
            info=info_.split('/')
            try:
              if match:=re.search(r'\d{4}(-\d{1,2}){0,2}', info_):
                publishTime=match.group()
                # ネブクロ / 新潮社 / 2022-10-7
              if info[-1].strip()==publishTime:
                # 作者1 / 新潮社 / 2022-10-7/ /
                info.append('')
              if match:=re.search(r'\d+\.\d+|\d+', info[-1]):
                price=info[-1].strip()
              if not publishTime and not price:
                # 作者1 / 新潮社
                info.append('')
                info.append('')
              elif (not publishTime or not price) and len(info)<=3:
                # 作者1 / 新潮社 
                info.append('')
              if len(info)>=3:
                publisher=info[-3].strip()
              if len(info)>=4:
                author='/'.join([i.strip() for i in  info[:-3]])
            except:
              print(info,'error')
        book=Book(title, author, desc, score, price, real_price, publisher,publishTime,tag)
        books.append(book.__dict__)
      BOOKS.insert_many(books).execute()
      logging.info(f'抓取完成-{page//20}-{tag}')
      repeat=0
      page+=20
      if page//20>=end:
        break
    except HTTPError as err:
      if repeat>5:
        logging.error(f'发生错误-{page//20}-{tag}-{str(err)}')
        break

def muilti_thread_spider(tag):
  url = 'https://book.douban.com/tag/'+urllib.parse.quote(tag)+f'?start={0}&type=T'
  headers = {
      'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
  }
  request = urllib.request.Request(url, headers=headers)
  with urllib.request.urlopen(request) as f:
    html_doc = f.read().decode('utf-8')
  soup = BeautifulSoup(html_doc,'lxml')
  paginator_a=soup.select('.paginator > a')
  if paginator_a and len(paginator_a)>0:
    max_page=int(paginator_a[-1].get_text().strip()) 
    # max_page=10
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
      results = executor.map(lambda page:tag_spider(tag,page,page+1), range(0,max_page))

    
def main():
  logging.info('spider start')
  muilti_thread_spider('美食')
  # 关闭连接
  db.close()
  logging.info('spider end')
  
if __name__ == '__main__':
    # 配置日志
  logging.basicConfig(
      filename='douban/app.log',  # 日志文件名
      level=logging.INFO,  # 日志级别
      format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
      encoding='utf-8'  # 文件编码
  )
  main()