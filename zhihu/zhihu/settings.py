# Scrapy settings for zhihu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "zhihu"
LOG_LEVEL ='INFO'
SPIDER_MODULES = ["zhihu.spiders"]
NEWSPIDER_MODULE = "zhihu.spiders"
DEPTH_LIMIT=0
# 启用自动限速
AUTOTHROTTLE_ENABLED = True
# 初始下载延时
AUTOTHROTTLE_START_DELAY = 2
# 在高并发情况下的最大延时
AUTOTHROTTLE_MAX_DELAY = 5
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "zhihu (+http://www.yourdomain.com)"

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'
DOWNLOAD_TIMEOUT=10
# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
   "cookie":'_xsrf=lTKAScHEpxF8Pm6h0qD1aI5KO9e46WMv; BEC=8b4a1b0a664dd5d88434ef53342ae417; __zse_ck=004_Gqy0M7jJAX34D3jw1UjpND9qoCUccMb0RMV6zJzCY6GLpHn8UIVnSd/XtM/IZwyXwOsBy5Xo0P5V=rLqQqglFSRUR7b3Q6PRF0TKG2JTu4JWXb4zK6Zvhn9m1Jm3Qt2M-FzFXnOBE90T+SIQFEziYIJBWyLo3FOBeadE10hfGYMSIQdC2j2YsjLKtFMKQXSLPToNQvfHROppo87FcB5yN/Gyknv0uzN5bD+CmiyU0H4vnJ/83LqLRIvkgWGoiS2xj'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'scrapy.spidermiddlewares.depth.DepthMiddleware': 900,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # "zhihu.middlewares.CustomHeadersMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "zhihu.pipelines.ZhihuPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
