#coding=utf-8
#!/usr/bin/python
import pymysql
from time import sleep, ctime
from bs4 import BeautifulSoup

from urllib import urlopen ,urlcleanup
import urllib2
import re
import time
import os
class kws():
    def __init__(self, domains, kw,start_url):
        self.domains = domains
        self.kw = kw
        self.url = start_url
        self.seen = set()#已经找过的链接
        self.q = set()
    #解析当前页面
    def parse_page(self,url):
        attempts = 0
        success = False

        req = urllib2.Request(url)
        req.add_header('Cache-Control', 'max-age=0')
        req.add_header("User-Agent",
                      "Mozilla/5.0 (X11; Linux x86_6) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.160 Safari/537.22")

        while attempts < 3 and not success:
            try:
                resp = urllib2.urlopen(req, timeout=10)
                self.soup = BeautifulSoup(resp.read(), "lxml")
                resp.close()
                success = True
            except StandardError, e:
                # return 1 #忽略超时等其他错误
                print 'except 34:', e
                attempts += 1
                if attempts == 3:
                    os._exit(0)

    #获取正文部分,仅限东方财富
    def get_content(self,url):
        self.parse_page(url)
        # print self.soup.find_all('p')
        print self.soup.find(class_='time').text
        print re.sub(r'''<[^>]+>''', '', str(self.soup.find(id='ContentBody')))

    #找到页面的所有的链接
    def find_all_links(self,url):
        self.parse_page(url)
        # for s in self.domains:
        div = self.soup.find(id = 'newsListContent')
        all_links = div.find_all(href=True, text = True)
        # , text = True
        # self.new_a_set = self.soup.find_all(href=re.compile(".com"), text=True)

        if len(self.kw )>0:  #标题关键字查找
            for l in all_links:
                if l["href"] not in self.seen:
                    for kw in self.kw:
                        if kw in l.string:
                            print l["href"],l.string
                            self.get_content(url=l["href"])
                            self.seen.add(l["href"])
                            break
        else:#查找所有 不需要匹配关键字
            for l in all_links:
                if l["href"] not in self.seen:
                    print l["href"], l.string
                    self.get_content(url=l["href"])
                    self.seen.add(l["href"])
        return

    # 找到前n页的链接，以东方财富http://finance.eastmoney.com/yaowen_cgjjj.html为起始链接
    def read_n_pages(self,n):
        self.find_all_links(url=self.url)
        url = self.url
        for i in range(2,n,1):
            temp = url.replace('.html', '_'+str(i)+'.html')
            # next_url = self.url
            print temp
            self.find_all_links(temp)
            sleep(1)

    def read_next_pages(self,url):
        try:
            div = self.soup.find(id="pagerNoDiv",recursive=True)
            next_page = div.find(href=True,recursive=True, text=u'下一页')
        except StandardError, e:
            print 'except 85:', e
            return

        print next_page["href"]
        index = url.rfind('/')

        next = url[0:index] +'/'+ next_page["href"]
        print next
        sleep(1)
        if next :
            self.find_all_links(url = next)
            # self.url = next
            self.read_next_pages(url=next)
        else:
            return #到最后一页了

class baidu_search(kws):
    def find_all_links(self, url):
        self.parse_page(url)
        for i in range(1,11,1):
            all_links = self.soup.find('table',id = str(i))
            print re.sub(r'''<[^>]+>''', '', str(all_links.find('a'))),re.sub(r'''<[^>]+>''', '', str(all_links.find('font')))
        return

def main():

    # k = kws(domains=[],kw=[],start_url = 'http://forex.eastmoney.com/news/cdhgd.html')
    # k.read_n_pages(n = 10)
    bd = baidu_search(domains=[], kw=[], start_url \
       = 'https://www.baidu.com/s?tn=baidurt&rtt=1&bsst=1&cl=3&ie=utf-8&bs=%E6%AC%A7%E6%B4%B2%E5%A4%AE%E8%A1%8C&f=8&rsv_bp=1&wd=%E8%8B%B1%E5%9B%BD%E5%A4%AE%E8%A1%8C&inputT=4700')
    bd.find_all_links(url=bd.url)

if __name__ == '__main__':
    main()