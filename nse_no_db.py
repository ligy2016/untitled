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
        for a in self.new_a_set:
            self.new_url_set.add(a["href"])
            self.urldict.setdefault(a["href"], []).append(a.string)
        self.new_urls = self.new_url_set.difference(self.pre_url_set)
        print "45",self.new_urls
        print len(self.new_url_set), len(self.pre_url_set), len(self.new_urls)

    def UpdateSet(self):
        print "54",self.pre_url_set
        print "55",self.new_url_set

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

        self.UpdateSet()

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
        div = self.soup.find(id='newsListContent')
        self.new_a_set = div.find_all(href=True, text=True)

def main():
    db = mysql.MYSQL(host = "127.0.0.1", user="root", pwd="123456", db="new_schema")
    # ss = SS_163(url = "http://money.163.com/",tablename = "urls")
    # ss_wallstreet = SS_Wallstreet(url = "http://wallstreetcn.com/",tablename = "urls")
    # ss_fx168 = SS_fx168(url = "http://www.fx168.com/forex/all/",tablename = "urls")

    dfcf_dhgd = DFCF_DHGD(url = "http://forex.eastmoney.com/news/cdhgd.html",tablename = "dfcf_dhgd")
    db.ConnectDB()

    dfcf_dhgd.pre_url_set = copy.deepcopy(set(db.SelectTopNUrls(tablename="dfcf_dhgd", n=20)))
    print dfcf_dhgd.pre_url_set
    while(1):
        # (tablename, urls, dict) = ss.gg()
        # mysql.SaveUrls( 'urls', urls, dict)
        # (tablename, urls, dict) = ss_wallstreet.gg()
        # mysql.SaveUrls( 'urls', urls, dict)
        # (tablename, urls, dict) = ss_fx168.gg()
        # mysql.SaveUrls( 'urls', urls, dict)
        dfcf_dhgd.gg()
        print (dfcf_dhgd.tablename, dfcf_dhgd.new_urls ,dfcf_dhgd.urldict)
        # db.SaveUrls(tablename, urls, dict)
        db.conn.commit()
        break
        sleep(300)

    db.DisconnectDB()

if __name__ == '__main__':
    main()