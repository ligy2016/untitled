#coding=utf-8
#!/usr/bin/python
import pymysql
from time import sleep, ctime
from bs4 import BeautifulSoup
# from urllib import urlopen ,urlcleanup
from urllib import urlopen ,urlcleanup
import urllib2
import re
import time
class kws():
    def __init__(self, domains, kw,start_url):
        self.domains = domains
        self.kw = kw
        self.url = start_url
        self.seen = set()#已经找过的链接
        self.q = set()
    #解析当前页面
    def parse_page(self,url):
        req = urllib2.Request(url)
        req.add_header('Cache-Control', 'max-age=0')
        try:
            resp = urllib2.urlopen(req, timeout=10)
            self.soup = BeautifulSoup(resp.read(), "lxml")
            resp.close()
        except StandardError, e:
            # return 1 #忽略超时等其他错误
            print 'except:', e
    #获取正文部分,仅限东方财富哈！
    def get_content(self):

        self.parse_page(self.url)

        # print self.soup.find_all('p')

        # print self.soup.find(id='ContentBody')

        print re.sub(r'''<[^>]+>''', '', str(self.soup.find(id='ContentBody')))


    #找到页面的所有的链接
    def find_all_links(self,url):
        self.parse_page(url)
        # for s in self.domains:
        all_links = self.soup.find_all(href=True, text = True)
        # , text = True
        # self.new_a_set = self.soup.find_all(href=re.compile(".com"), text=True)


        if self.kw is not None:  #标题匹配关键字查找
            for l in all_links:
                if l["href"] not in self.seen:
                    for kw in self.kw:
                        if kw in l.string:
                            print l["href"],l.string
                            self.seen.add(l["href"])
                            break
        else:#查找所有 不需要匹配关键字
            for l in all_links:
                if l["href"] not in self.seen:
                    print l["href"], l.string
                    self.seen.add(l["href"])
                    break
        return

    # 找到前n页的链接，以东方财富http://finance.eastmoney.com/yaowen_cgjjj.html为起始链接
    def read_n_pages(self,n):
        url = self.url
        for i in range(2,n,1):
            temp = url.replace('.html', '_'+str(i)+'.html')
            # next_url = self.url
            print temp
            self.find_all_links(temp)
            sleep(1)

def main():

    k = kws(domains=[],kw=[u'原油',u'美元'],start_url = 'http://finance.eastmoney.com/news/1374,20161130688996750.html')
    # k.read_n_pages(15)
    k.get_content()

if __name__ == '__main__':
    main()