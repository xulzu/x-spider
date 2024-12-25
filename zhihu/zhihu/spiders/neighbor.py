import json
from urllib.parse import parse_qs, urlencode, urlparse
import scrapy
import undetected_chromedriver as uc
from scrapy.http import JsonRequest
from selenium import webdriver
from zhihu.items import PeopleItem, RelationItem
class NeighborSpider(scrapy.Spider):
    name = "neighbor"
    start_urls=['https://www.zhihu.com/people/weizhi-xiazhi']
    chromeDriver=None
    x_zse_96_list=[]
    def parse(self, response):
        js_initialData=response.css('script[id="js-initialData"]::text').get()
        json_data = json.loads(js_initialData)
        users=json_data.get('initialState',{}).get('entities',{}).get('users',{})
        userInfo= list(users.values())[0]
        if userInfo:
          print(userInfo.get('urlToken',''),'------parse')
          location=''
          for loc in userInfo.get('locations', []):
            location+=loc.get('name', '')
          education=''
          for edu in userInfo.get('educations', []):
            education+=edu.get('entranceYear', '年份unknown').__str__() +' '+ edu.get('school', {}).get('name', '')+' '+edu.get('major', {}).get('name', '')
            education=education.strip()   
          employments=''
          for emp in userInfo.get('employments', []):
            employment=emp.get('company', {}).get('name', '')+' '+emp.get('job', {}).get('name', '')
            employments+=employment.strip()            
         
          yield PeopleItem(
              name =userInfo.get('name',''),
              url_token = userInfo.get('urlToken',''),
              location = location,
              business =userInfo.get('business',{}).get('name',''),
              gender = userInfo.get('gender',''),
              employment = employments,
              education = education,
              avatar_url = userInfo.get('avatarUrl',''),
              description = userInfo.get('description',''),
              headline = userInfo.get('headline',''),
          )
          level=response.meta.get('level', 0)
          # 暂时只爬取一层
          if level < 1:
            meta={
              'level':level,
              'p-token':userInfo["urlToken"]
            }
            # 关注列表
            yield scrapy.Request(url=f'https://www.zhihu.com/api/v4/members/{userInfo["urlToken"]}/followees',meta=meta.copy(), callback=self.followees_parse)
            followerCount=userInfo.get('followerCount', 0)
            self.initChrome()
            with open('zhihu/chrome/parse_x_zse_96.js','r',encoding='utf-8') as f:
              js = f.read()
              self.x_zse_96_list=self.chromeDriver.execute_script(js,userInfo["urlToken"], followerCount)
              # 被关注列表
              request=self.get_request(userInfo["urlToken"], 0)
              yield scrapy.Request(url=request['url'],headers=request['headers'],meta=meta.copy(), callback=self.followers_parse)
    def get_request(self,token,offset):
      return {
        'url':f'https://www.zhihu.com/api/v4/members/{token}/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&offset={offset}&limit=20',
        'headers':{
          'x-zse-96':'2.0_'+self.x_zse_96_list[offset//20],
          'x-zse-93':'101_3_3.0',
          'cookie':'_xsrf=g1ulEqx9lWbA9NmLSSaCIjOMR3BW5MVg; _zap=184586e4-9ce1-4d16-a639-7523929888f8; d_c0=AGDSHoNAnBmPTs1EWLYJ0KRD_THbLLxwYfY=|1732762623; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1732757156,1733103204,1733733392,1733814746; HMACCOUNT=B01B9F0025190A91; captcha_ticket_v2=2|1:0|10:1733816702|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfQmV1bEZSQzB0M2J4ZW5wYiozcXJJV1dtZHFuZG11QmxoaVFpa21ieTQyZjFWTDI4LlhDOEhGX1h0dV9OV3AqQTUzT0hOY1FsbW9ieUtNM3RjNV9iRzZzR0o1RVRIMm5jRzRhNVVFdFlpSWpER1BSWU96UFdlVk11bmhyRUMxWDNsOWEwUWVUMWFCVG5fMXA1TFF1TF9uQklieTZoRE9teDBGbUVKNW5zcFhlcVliOEZxY0hPbUNVRnAqVDVTV001OUxKRUhUNjNTTUxsVzUwaWkzMTBGLmJUTDZUenNjazNVVVlZTHl5VHhhaUQwejBRdVlRSGg1aFNyQ3g2d1ltMlJiUHFWR3FqUktjOGZlZUtDV3JRb1dNVWpFYVdrMHRELjNXZm9EQ1UwWnhoYmx0d244SHdJOFo0cWRId19nRHNNeVRSM0VSa1NYbTYzY3JZeHR1TmpDSE1UbkE1SnowTU8uWUhlcUVsb0ZrTzJNY1poQ1FmbUxsRnhaKmxyRkEyQjB0bXhUaGFCNE4wTkoxUVpfdDFyWndZV2xaX1R2VnZ4NHhxM2ZvVzRWYVpvRTFLRENIV2lPOU1KajBhVW1idVliTFd3S3E0dmFTdnlfZGNTMlhNTUFFY25XKjVJZ0xxZDAqd0FETmY5MDNaTUoyLnhyRl90UldXVTh0VDZKUXpYSXhHeFg3N192X2lfMSJ9|c24422ce84cc61f5cfe9f4cf780636c00255ceb62bf3bcb43c4efdb671a26f45; __zse_ck=004_wEDGm34SLxFuHdWo0xJ0SoCNaipv/IBVXZ2SU0tr0TecqIP5iulgbNI1iIZWyjRZCcTS7lzN/7Qms0=bEkYC9ZHrRrpclyhqx0AjgebiAjwpTwxuJKMfIOGuJ5vPnkEb-nUv82HL2im2xyjPTm/puGjhWOU2auNSzypxAo2xnEcrlCTgTD31yv2xdojsRm1Ib1NjMgOP9Kaxjyqp3kjM7ffXF+zL9E2Iv9xpGu2eLPLxGGfYolM8AsH0+PMWcigY0; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1734506390; captcha_session_v2=2|1:0|10:1734506390|18:captcha_session_v2|88:YnIrTUxaN3lFMm9Jemd2TjllOXluYmRMYjZoRHBkcCt1ak1uZEJJdVhpTzBEYm4zZHN2b0hVdEN3SnBRT0pFWA==|f11c514cb6ce91948b376aed30c683f6f57784deb4e99667358283e87e26eff8; gdxidpyhxdE=mPeeVXVuTyp1Kv0l5xV4X%2Fb9RDOo74xejgNREzHZeT1WqczBDrxipAysvJuGCS%2BCH1U50JvIZo1QD4Jo7%2BV%2FrcxB14z9S9gn%2FrRRmnSJicvqNKCtDSEXstud5MQpCiQyYWk2e%2FYc1wzCn%2FDt%5CorgyeCHDhQvXM0oZJeLnYmrOk9dd%5CqR%3A1734507292115; BEC=5468d338557f9906d5c8cdb6d5cda0d3'
        }
      }
    def followees_parse(self, response):
        res=json.loads(response.text)
        data=res.get('data', [])
        paging=res.get('paging', {})
        is_end=paging.get('is_end', False)
        p_token=response.meta.get('p-token', '')
        next=paging.get('next', '')
        level=response.meta.get('level')
        print(p_token,'------followees_parse')
        for user in data:
          url_token=user.get('url_token', '')
          if url_token:
            yield RelationItem(
              left_url_token=p_token,
              right_url_token=url_token,
              relation_type=1
            )
            meta=response.meta.copy()
            meta['level']=level+1
            yield scrapy.Request(url=f'https://www.zhihu.com/people/{url_token}',meta=meta)
        if not is_end:
          yield scrapy.Request(url=next, meta=response.meta, callback=self.followees_parse)
    def followers_parse(self, response):
        res=json.loads(response.text)
        data=res.get('data', [])
        paging=res.get('paging', {})
        is_end=paging.get('is_end', False)
        p_token=response.meta.get('p-token', '')
        next=paging.get('next', '')
        parsed_url = urlparse(next)
        query_string = parsed_url.query
        params = parse_qs(query_string)
        level=response.meta.get('level')
        for user in data:
          url_token=user.get('url_token', '')
          if url_token:
            yield RelationItem(
              left_url_token=p_token,
              right_url_token=url_token,
              relation_type=2
            )
            meta=response.meta.copy()
            meta['level']=level+1
            yield scrapy.Request(url=f'https://www.zhihu.com/people/{url_token}',meta=meta)
        if not is_end:
          offset_next = int(params.get('offset', [None])[0])
          print(p_token,offset_next,'------followers_parse')
          request=self.get_request(p_token, offset_next)
          yield scrapy.Request(url=request['url'],headers=request['headers'],meta=response.meta, callback=self.followers_parse)

    def initChrome(self):
      if self.chromeDriver:
        return
      options=webdriver.ChromeOptions()
      options.add_argument('--headless=new')
      options.add_argument("start-maximized")
      options.add_argument('--disable-blink-features=AutomationControlled')
      options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
      driver = webdriver.Chrome(options=options)
      driver.get('http://127.0.0.1:5501/index.html')
      self.chromeDriver=driver
      
        
