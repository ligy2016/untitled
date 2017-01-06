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
    def __init__(self,url,tablename):
        self.url = url
        self.tablename = tablename
        self.urldict = {}
        self.a_set = set()
        self.pre_url_set = set()
        # self.new_a_set = set()
        self.new_urls = set()
        self.new_url_set = set()
        self.soup = BeautifulSoup( "lxml")

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

    def FindPattern(self):
        self.new_a_set = self.soup.find_all(href=re.compile(".com"), text=True)

    def GetNewLinks(self):
        self._UpdateSet()
        for a in self.new_a_set:
            self.new_url_set.add(a["href"])
            self.urldict.setdefault(a["href"], []).append(a.string)
        self.new_urls = self.new_url_set.difference(self.pre_url_set)
        for url in self.new_urls: #打印显示每次新发现的链接
            print ctime(),self.urldict.get(url, 'not found')[0].strip(),url
        # print len(self.new_url_set), len(self.pre_url_set), len(self.new_urls)

    def _UpdateSet(self):

        if(len(self.new_url_set) >0):
            self.pre_url_set = copy.deepcopy(self.new_url_set)
        self.new_url_set.clear()
        self.urldict.clear()
        self.new_urls.clear()

    def gg(self):
        ret = self.GetSiteContent()
        if ret == 1:
            return (None,None,None)
        self.FindPattern()
        self.GetNewLinks()
        # self.UpdateSet()

class SS_163(ScrawlSite):
    def FindPattern(self):
        self.new_a_set = self.soup.find_all(href=re.compile("163.com"), text=True)

class SS_Wallstreet(ScrawlSite):
    def FindPattern(self):
        self.new_a_set = self.soup.find_all(href=re.compile("node"), text=True)

class SS_fx168(ScrawlSite):
    def FindPattern(self):
        self.new_a_set = self.soup.find_all(href=re.compile("fx168"), text=True)
class DFCF_DHGD(ScrawlSite):#东方财富大行观点
    def FindPattern(self):
        try:
            div = self.soup.find(id='newsListContent')
            self.new_a_set = div.find_all(href=True, text=True)
        except StandardError,e:
            print e

class DFCF_USD(ScrawlSite):  # 东方财富美元
    def FindPattern(self):
        div = self.soup.find(id='newsListContent')
        self.new_a_set = div.find_all(href=True)

    def GetNewLinks(self):
        self._UpdateSet()
        for a in self.new_a_set:
            self.new_url_set.add(a["href"])
            title = re.sub(r'''<[^>]+>''', '', str(a))
            self.urldict.setdefault(a["href"], []).append(title)
        self.new_urls = self.new_url_set.difference(self.pre_url_set)
        for url in self.new_urls:  # 打印显示每次新发现的链接
            print ctime(), self.urldict.get(url, 'not found')[0].strip(), url
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
    db = mysql.MYSQL(host = "127.0.0.1", user="root", pwd="123456", db="new_schema")
    db.ConnectDB()

    dfcf_dhgd = DFCF_DHGD(url = "http://forex.eastmoney.com/news/cdhgd.html",tablename = "dfcf_dhgd")
    dfcf_whpl = DFCF_WHPL(url="http://forex.eastmoney.com/news/cwhpl.html", tablename="dfcf_whpl")
    dfcf_usd = DFCF_USD(url="http://forex.eastmoney.com/news/aUSD.html", tablename="dfcf_usd")
    dfcf_jpy = DFCF_JPY(url="http://forex.eastmoney.com/news/aJPY.html", tablename="dfcf_jpy")
    dfcf_eur = DFCF_EUR(url="http://forex.eastmoney.com/news/aEUR.html", tablename="dfcf_eur")
    dfcf_gbp = DFCF_GBP(url="http://forex.eastmoney.com/news/aGBP.html", tablename="dfcf_gbp")
    dfcf_aud = DFCF_AUD(url="http://forex.eastmoney.com/news/aAUD.html", tablename="dfcf_aud")
    dfcf_nzd = DFCF_NZD(url="http://forex.eastmoney.com/news/aNZD.html", tablename="dfcf_nzd")

    dfcf_dhgd.pre_url_set = copy.deepcopy(set(db.SelectTopNUrls(tablename="dfcf_dhgd", n=20)))

    while(1):
        dfcf_dhgd.gg()
        db.SaveUrls(dfcf_dhgd.tablename, dfcf_dhgd.new_urls, dfcf_dhgd.urldict)

        dfcf_whpl.gg()
        db.SaveUrls(dfcf_whpl.tablename, dfcf_whpl.new_urls, dfcf_whpl.urldict)

        dfcf_usd.gg()
        db.SaveUrls(dfcf_usd.tablename, dfcf_usd.new_urls ,dfcf_usd.urldict)

        dfcf_jpy.gg()
        db.SaveUrls(dfcf_jpy.tablename, dfcf_jpy.new_urls, dfcf_jpy.urldict)

        dfcf_eur.gg()
        db.SaveUrls(dfcf_eur.tablename, dfcf_eur.new_urls, dfcf_eur.urldict)

        dfcf_gbp.gg()
        db.SaveUrls(dfcf_gbp.tablename, dfcf_gbp.new_urls, dfcf_gbp.urldict)

        dfcf_aud.gg()
        db.SaveUrls(dfcf_aud.tablename, dfcf_aud.new_urls, dfcf_aud.urldict)

        dfcf_nzd.gg()
        db.SaveUrls(dfcf_nzd.tablename, dfcf_nzd.new_urls, dfcf_nzd.urldict)


        db.conn.commit()
        # break
        sleep(300)

    db.DisconnectDB()

if __name__ == '__main__':
    main()