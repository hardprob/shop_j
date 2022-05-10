# import scrapy
# import re
# from scrapy_splash import SplashRequest
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium import webdriver
# from jdsc.items import JdscItem,General_Category,Subclass
# import threading
# import time
# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--load-images=false')
# chrome_options.add_argument('--disable-gpu')#上面三行代码就是为了将Chrome不弹出界面，实现无界面爬取
# brower = webdriver.Chrome(chrome_options=chrome_options)
# wait=WebDriverWait(brower,10)
# brower.maximize_window()
#
# # splash.scroll_position = {x=..., y=...}
# # splash.resource_timeout = 600.0
# script = """
# assert(splash:go(args.url))
# splash:set_user_agent("Mozilla/5.0")
# splash:runjs("document.documentElement.scrollTop=10000")
# splash.images_enabled = false
# splash:on_request(function(request)
#     filters=nofonts,easylist
#     if first then
#         request:set_timeout(2)
#         first = false
#     end
#     if request.url:find('ad_ids') ~= nil then
#         request:abort()
#     end
# end)
# return {html = splash:html()}
# """
#
# class JdSpider(scrapy.Spider):
#     name = 'jd1'
#     allowed_domains = ['.jd.com']
#     start_urls = ['https://www.jd.com/allSort.aspx']
#     # start_urls = ['http://localhost:8050/render.html?url=https://item.jd.com/100014348492.html']
#     # start_urls = ['https://list.jd.com/list.html?cat=9987,653,655']
#     def make_requests_from_url(self, url):
#         # return scrapy.Request(url,callback=self.spxq)
#         return SplashRequest(url, callback=self.parse, args={'lua_source': script})
#
#         # return scrapy.Request(url, callback=self.spxq)
#
#     def parse(self, response):#所有类别的url
#         a=response.xpath('/html/body/div[5]/div[2]/div[1]/div[2]/div/div/div[2]/div[3]/dl/dd/a/@href').getall()
#         self.logger.debug(a)
#         item1 = General_Category()
#         for i in a[20:25]:
#             url='https:'+i
#             item1['URL']=url
#             self.get_url(url)
#             # t = threading.Thread(target=self.get_url(url), args=("t1",))
#             # t.start()
#
#     def get_url(self,url):
#         try:
#             brower.get(url)
#             self.paser_next()
#         except TimeoutException:
#             return self.get_url(url)
#
#     def paser_next(self):
#         try:
#             submit = wait.until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "#key")))
#             submit.click()
#             brower.execute_script("document.documentElement.scrollTop=10000")
#             time.sleep(5)
#             html = brower.page_source
#
#             submit1 = wait.until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "#J_bottomPage > span.p-num > a.pn-next")))
#             self.paser_url(html)
#             submit1.click()
#             return self.paser_next()
#         except TimeoutException:
#             return self.paser_next()
#
#     def paser_url(self,html):
#         b = list(set(re.findall('<a target="_blank" title=.*?href="(//item.jd.com/.*?)" onclick=', html, re.S)))
#         item2 = Subclass()
#         for i in b[:2]:
#             url = 'http://localhost:8050/render.html?url=https:' + i
#             item2['URL'] = url
#             yield scrapy.Request(url, callback=self.spxq)
#     #         yield SplashRequest(url,callback=self.spxq,endpoint='run',args={'lua_source': script})
#
#     def spxq(self,response):
#         # self.logger.debug(response.text)
#         spdetail={
#             'title':response.xpath('/html/body/div[6]/div/div[2]/div[1]/text()').getall(),
#             'price':response.xpath('/html/body/div[6]/div/div[2]/div[3]/div/div[1]/div[2]/span[1]/span[2]/text()').get(),
#             'evaluate':response.xpath('//*[@id="comment-count"]/a/text()').get(),
#             'parameter':response.xpath('//*[@id="detail"]/div[2]/div[1]/div[1]').xpath('string(.)').extract()
#         }
#         self.logger.debug(spdetail)
#         item = JdscItem()
#         for field in item.fields:
#             item[field] = spdetail[field]
#         cc=response.xpath('//*[@id="choose-attr-1"]/div[1]/text()').getall()
#         if cc==[]:
#             pass
#         else:
#             cc_list=response.xpath('//*[@id="choose-attr-1"]/div[2]/div/text()').getall()
#             for i in cc_list:
#                 url='https://item.jd.com/{}.html'.format(i)
#                 yield SplashRequest(url=url,callback=self.spxq,endpoint='run',args={'lua_source': script})
#
#
#
#
#
#
#
#
#
#
#
import random
ua=['Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0',
    ' Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1']
useragent=random.choice(ua)
print(useragent)