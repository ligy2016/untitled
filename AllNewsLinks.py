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
        attempts = 0
        success = False
        req = urllib2.Request(self.url)
        req.add_header('Cache-Control', 'max-age=0')
        while attempts < 3 and not success:
            try:
                resp = urllib2.urlopen(req, timeout=10)
                self.soup = BeautifulSoup(resp.read(), "lxml")
                resp.close()
                success = True
            except StandardError, e:
                attempts += 1
                print 'except', e
                if attempts == 3:
                    # os._exit(0)
                    return 1 #忽略超时等其他错误

    def FindNewsLinks(self):
        try:
            div = self.soup.find(id='newsListContent')
            self.a_set = div.find_all(href=True, text=True)
        except StandardError, e:
            print e
    def SaveNewsLinks(self):
        for a in self.a_set:
            self.db.SaveContent(self.tablename, a["href"].strip(), a.string.strip(),str_date=self.getdate(url=a["href"]))
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
    def getdate(self,url):
        # url ='http://futures.eastmoney.com/news/1516,20170108700852468.html '
        index = url.find(',')
        date = url[index+1:index+9]
        return date



class DFCF_DHGD(ScrawlSite):#东方财富大行观点+
    pass


class DFCF_USD(ScrawlSite):  # 东方财富美元
    def FindNewsLinks(self):
        try:
            div = self.soup.find(id='newsListContent')
            self.a_set = div.find_all(href=True)
        except StandardError, e:
            print e
    def SaveNewsLinks(self):
        for a in self.a_set:
            # print str(a.contents).decode("unicode_escape")
            self.db.SaveContent(self.tablename, a["href"].strip(), a.find(name='span', attrs={'class','list-content'}).text.strip(),str_date=self.getdate(url=a["href"]))

class DFCF_ZHZX(ScrawlSite):  # 东方财富期货综合咨询
    def FindNewsLinks(self):
        try:
            div = self.soup.find(id='newsListContent')
            div_text = div.find_all(name='div', attrs={'class', 'text'})
            for item in div_text:
                link = item.find(name='a')["href"]
                title = item.find(name='a').string.strip()
                # time = item.find(name='p',attr={'class','time'}).text.strip()
                date = self.getdate(url=link)
                self.db.SaveContent(tablename=self.tablename, url=link,title=title,str_date=date)
        except StandardError, e:
            print e
class DFCF_WHPL(DFCF_DHGD):
    pass

def main():

    dfcf_dhgd = DFCF_DHGD(url = "http://forex.eastmoney.com/news/cdhgd.html",tablename = "dfcf_dhgd", n = 2)
    dfcf_whpl = DFCF_DHGD(url="http://forex.eastmoney.com/news/cwhpl.html", tablename="dfcf_whpl",n=2)
    dfcf_usd = DFCF_USD(url="http://forex.eastmoney.com/news/aUSD.html", tablename="dfcf_usd",n=10)
    # dfcf_jpy = DFCF_USD(url="http://forex.eastmoney.com/news/aJPY.html", tablename="dfcf_jpy",n=1)
    # dfcf_eur = DFCF_USD(url="http://forex.eastmoney.com/news/aEUR.html", tablename="dfcf_eur",n=1)
    # dfcf_gbp = DFCF_USD(url="http://forex.eastmoney.com/news/aGBP.html", tablename="dfcf_gbp",n=1)
    # dfcf_aud = DFCF_USD(url="http://forex.eastmoney.com/news/aAUD.html", tablename="dfcf_aud",n=10)
    # dfcf_nzd = DFCF_USD(url="http://forex.eastmoney.com/news/aNZD.html", tablename="dfcf_nzd",n=10)
    # 期货导读
    dfcf_qhdd = DFCF_ZHZX(url="http://futures.eastmoney.com/news/cqhdd.html", tablename="dfcf_qhdd",n=4)
    # 焦点观察
    dfcf_jdgc = DFCF_ZHZX(url="http://futures.eastmoney.com/news/cjdgc.html", tablename="dfcf_jdgc", n=10)
    # 综合资讯
    dfcf_zhzx = DFCF_ZHZX(url="http://futures.eastmoney.com/news/czhzx.html", tablename="dfcf_zhzx", n=3)

    dfcf_whpl.read_n_pages()

if __name__ == '__main__':
    main()