from scrapy import cmdline
import os

proj=os.path.join(os.getcwd(),'guba')
os.chdir(proj)
cmdline.execute("scrapy crawl title_spider".split())