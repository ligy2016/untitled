#coding=utf-8
#!/usr/bin/python
import pymysql
from time import sleep, ctime
from bs4 import BeautifulSoup
from urllib import urlopen ,urlcleanup


class kws():
    def __init__(self, domains, kw):
        self.domains = domains
        self.kw = kw

    #解析当前页面
    def parse_page(self):
        req = urllib2.Request(self.url)
        req.add_header('Cache-Control', 'max-age=0')
        try:
            resp = urllib2.urlopen(req, timeout=10)
        except :
            # return 1 #忽略超时等其他错误
            pass
        self.soup = BeautifulSoup(resp.read(), "lxml")
        resp.close()
    #判断新的连接是否在指定域内
    def isindomain(self,link):
        for domain in self.domains:
            print domain,link
            # print link
            if domain in link:
                return True
        return False
    #找到当前页面的所有的链接
    def find_all_links(self):
        for s in self.domains
            self.new_a_set += self.soup.find_all(href=re.compile(s), text=True)
            # self.new_a_set = self.soup.find_all(href=re.compile(".com"), text=True)
        return
    def link_is_searched(self):
        if link in oldlinks
            return True

    def keyword():
        pass

def main():
    domains = ['163','sina']
    k = kws(domains=domains,kw='希拉里')
    if(k.isindomain('sina.com')):
        print 'true'
    else:
        print 'false'
if __name__ == '__main__':
    main()