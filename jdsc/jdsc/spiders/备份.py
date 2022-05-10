import re
import scrapy
from jdsc.items import JdscItem
from redis import Redis
from jdsc.settings import *


class JdSpider(scrapy.Spider):
    # name = 'jd2'
    # allowed_domains = ['.jd.com']
    start_urls = ['https://www.jd.com/allSort.aspx']
    conn = Redis(host=ip, port=6379, password='123456a')

    def parse(self, response):  # 所有类别的url
        leibie_list = response.xpath(
            '/html/body/div[5]/div[2]/div[1]/div[2]/div/div/div[2]/div[3]/dl/dd/a/@href').getall()
        for i in leibie_list:
            b = re.findall('//list.jd.com/list.html\?cat=(.*?),(.*?),(.*)', i)
            if b == []:
                pass
            else:
                url = 'https://list.jd.com/listNew.php?cat={}%2C{}%2C{}&page=1&s=1&click=0'.format(b[0][0], b[0][1],
                                                                                                   b[0][2])
                header = {
                    'referer': 'https://list.jd.com/list.html',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                }
                yield scrapy.Request(url, callback=self.parse2, headers=header)

    def parse2(self, response):  # 类别下所有商品
        sp_list = response.xpath('//*[@id="J_goodsList"]/ul/li')
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
        self.conn.sadd('jdscurls', response.url)

        if len(sp_list) < 30:
            self.logger.debug('没了')
        else:
            pg = int(re.findall('.*?page=(.*?)&.*', response.url)[0])
            self.logger.debug(str(pg))
            self.logger.debug('--------------------------------------')
            url = re.findall('(https.*?page).*', response.url)[0] + '={}&s={}&click=0'.format(str(pg + 1),
                                                                                              str(30 * pg - 3))
            header = {
                'referer': 'https://list.jd.com/list.html',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }
            yield scrapy.Request(url, callback=self.parse2, headers=header)







