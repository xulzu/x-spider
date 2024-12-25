from scrapy import cmdline
import os

proj=os.path.join(os.getcwd(),'zhihu')
os.chdir(proj)
cmdline.execute("scrapy crawl neighbor ".split())