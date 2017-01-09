#coding=utf-8
#!/usr/bin/python
from time import sleep, ctime
from bs4 import BeautifulSoup
from urllib import urlopen ,urlcleanup
import urllib2
import sys
import re
import time
import copy
import mysql

reload(sys)
sys.setdefaultencoding('utf-8')
class ScrawlSite():
    def __init__(self,url,tablename,n):
        self.n = n
        self.url = url
        self.tablename = tablename
        self.a_set = set()
        self.soup = BeautifulSoup( "lxml")
        self.db = mysql.MYSQL(host="127.0.0.1", user="root", pwd="123456", db="new_schema")
        self.db.ConnectDB()

    def GetSiteContent(self):
        req = urllib2.Request(self.url)
        req.add_header('Cache-Control', 'max-age=0')
        try:
            resp = urllib2.urlopen(req, timeout=10)
            self.soup = BeautifulSoup(resp.read(), "lxml")
            resp.close()
        except StandardError, e:
            print 'except', e
            return 1 #忽略超时等其他错误

    def FindNewsLinks(self):
        try:
            div = self.soup.find(id='newsListContent')
            self.a_set = div.find_all(href=True, text=True)
        except StandardError, e:
            print e
    def SaveNewsLinks(self):
        for a in self.a_set:
            self.db.SaveContent(self.tablename, a["href"].strip(), a.string.strip())
    # 找到前n页的链接，以东方财富http://finance.eastmoney.com/yaowen_cgjjj.html为起始链接
    def read_n_pages(self):
        url = self.url
        self.gg()
        for i in range(2,self.n+1,1):
            self.url = url.replace('.html', '_'+str(i)+'.html')
            print self.url
            self.gg()
        self.db.DisconnectDB()
    def gg(self):
        ret = self.GetSiteContent()
        if ret == 1:
            return (None,None,None)
        self.FindNewsLinks()
        self.SaveNewsLinks()
        self.db.conn.commit()


class DFCF_DHGD(ScrawlSite):#东方财富大行观点
    def FindPattern(self):
        try:
            div = self.soup.find(id='newsListContent')
            self.a_set = div.find_all(href=True, text=True)
        except StandardError,e:
            print e

class DFCF_USD(ScrawlSite):  # 东方财富美元
    def FindPattern(self):
        div = self.soup.find(id='newsListContent')
        self.new_a_set = div.find_all(href=True)

class DFCF_WHPL(DFCF_DHGD):
    pass
class DFCF_JPY(DFCF_USD):
    pass
class DFCF_EUR(DFCF_USD):
    pass
class DFCF_GBP(DFCF_USD):
    pass
class DFCF_AUD(DFCF_USD):
    pass
class DFCF_NZD(DFCF_USD):
    pass

def main():

    dfcf_dhgd = DFCF_DHGD(url = "http://forex.eastmoney.com/news/cdhgd.html",tablename = "dfcf_dhgd", n = 1)
    # dfcf_whpl = DFCF_WHPL(url="http://forex.eastmoney.com/news/cwhpl.html", tablename="dfcf_whpl")
    # dfcf_usd = DFCF_USD(url="http://forex.eastmoney.com/news/aUSD.html", tablename="dfcf_usd")
    # dfcf_jpy = DFCF_JPY(url="http://forex.eastmoney.com/news/aJPY.html", tablename="dfcf_jpy")
    # dfcf_eur = DFCF_EUR(url="http://forex.eastmoney.com/news/aEUR.html", tablename="dfcf_eur")
    # dfcf_gbp = DFCF_GBP(url="http://forex.eastmoney.com/news/aGBP.html", tablename="dfcf_gbp")
    # dfcf_aud = DFCF_AUD(url="http://forex.eastmoney.com/news/aAUD.html", tablename="dfcf_aud")
    # dfcf_nzd = DFCF_NZD(url="http://forex.eastmoney.com/news/aNZD.html", tablename="dfcf_nzd")

    dfcf_dhgd.read_n_pages()

if __name__ == '__main__':
    main()