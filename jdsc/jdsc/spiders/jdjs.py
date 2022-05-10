import re
import scrapy
from jdsc.items import JdscItem
from redis import Redis
from jdsc.settings import *
import time
class JdSpider(scrapy.Spider):
    name = 'jd2'
    start_urls = ['https://www.jd.com/allSort.aspx']
    conn = Redis(host=ip, port=6379, password='123456a')
    def parse(self, response):#所有类别的url
        leibie_list=response.xpath('/html/body/div[5]/div[2]/div[1]/div[2]/div/div/div[2]/div[3]/dl/dd/a/@href').getall()
        for i in leibie_list[60:]:
            b=re.findall('//list.jd.com/list.html\?cat=(.*?),(.*?),(.*)',i)
            if b==[]:
                pass
            else:
                c=list(b[0])
                c.append(str(1))
                while 1:
                    ex = self.conn.sismember('jdscurls', str(c))
                    if ex == 1 :
                        self.log(str(c) + "已经爬取")
                        c[3]=str(int(c[3])+1)
                    else:
                        if (int(c[3]) == 1):
                            url='https://list.jd.com/list.html?cat={}%2C{}%2C{}&page=1&s=1&click=0'.format(c[0],c[1],c[2])
                            yield scrapy.Request(url, callback=self.parse2)
                        else:
                            if (int(c[3]) % 2 == 1):
                                url = 'https://list.jd.com/listNew.php?cat={}%2C{}%2C{}&page={}&s={}&scrolling=y&log_id={}&tpl=3_M&isList=1&show_items='.format(
                                    c[0], c[1], c[2], int(c[3]) + 1, int(c[3]) * 30 - 3, time.time() * 1000)
                                header = {
                                    'referer': response.url,
                                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                                    'x-requested-with': 'XMLHttpRequest',
                                }

                                yield scrapy.Request(url, callback=self.parse2, headers=header)

                            else:
                                url = 'https://list.jd.com/listNew.php?cat={}%2C{}%2C{}&page={}&s={}&click=0'.format(
                                    c[0], c[1], c[2], int(c[3]) + 1, int(c[3]) * 30 - 3)
                                yield scrapy.Request(url, callback=self.parse2)
                            break
    def parse2(self,response):#类别下所有商品
        c = re.findall('.*?cat=(.*?)%2C(.*?)%2C(.*?)&page=(.*?)&s=.*', response.url)
        if (int(c[0][3])%2==1):
            sp_list = response.xpath('//*[@id="J_goodsList"]/ul/li')
        else:
            sp_list =response.xpath('/html/body/li')
        self.log(len(sp_list))
        for i in sp_list:
            url1 = i.xpath('div/div[1]/a/@href').re('\/\/(item.jd.com/.*)')
            if url1 == []:
                pass
            else:
                shangping = {
                    'price': i.css('.p-price').xpath('strong/i/text()').get(),
                    'url': i.css('.p-img').xpath('a/@href').get(),
                    'title': str(i.css('.p-name').xpath('a//text()').getall()).replace('[', '').replace(']',
                                                                                                        '').replace(
                        '\\t', '').replace('\\n', '').replace('\'', '').replace(',', ''),
                    'youhui': i.css('.p-icons').xpath('i//text()').getall()
                }
                item = JdscItem()
                for field in item.fields:
                    item[field] = shangping[field]
                yield item
        self.conn.sadd('jdscurls', str(list(c[0])))
        if len(sp_list) < 30:
            self.logger.debug('没了')
        else:
            # 判断上页类型，根据类型确定下页走向

            b = re.findall('.*?cat=(.*?)%2C(.*?)%2C(.*?)&page=(.*?)&s=.*', response.url)
            if (int(b[0][3])>200):
                pass
            else:
                if(int(b[0][3])%2==1):
                    url='https://list.jd.com/listNew.php?cat={}%2C{}%2C{}&page={}&s={}&scrolling=y&log_id={}&tpl=3_M&isList=1&show_items='.format(b[0][0],b[0][1],b[0][2],int(b[0][3])+1,int(b[0][3])*30-3,time.time()*1000)
                    header={
                        'referer':response.url,
                        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                        'x-requested-with':'XMLHttpRequest',
                    }

                    yield scrapy.Request(url, callback=self.parse2, headers=header)
                else:
                    url='https://list.jd.com/list.html?cat={}%2C{}%2C{}&page={}&s={}&click=0'.format(b[0][0],b[0][1],b[0][2],int(b[0][3])+1,int(b[0][3])*30-3)
                    yield scrapy.Request(url, callback=self.parse2)
















