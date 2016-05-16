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


reload(sys)
sys.setdefaultencoding('utf-8')
class scrawl_site():
    def __init__(self,url):
        self.url = url
        self.urldict = {}
        self.a_set = set()
        self.url_set = set()
        self.new_a_set = set()
        self.new_url_set = set()
        self.soup = BeautifulSoup()

    def GetSiteContent(self):
        req = urllib2.Request("http://money.163.com/")
        req.add_header('Cache-Control', 'max-age=0')
        resp = urllib2.urlopen(req)
        self.soup = BeautifulSoup(resp.read(), "lxml")

    def FindPattern(self):
        self.new_a_set = self.soup.find_all(href=re.compile("163.com"), text=True)
    def SaveContent(self):
        for a in self.new_a_set:
            self.new_url_set.add(a["href"])
            self.addUrl(urldict, a["href"], a.string)

        new_urls = self.new_url_set.difference(url_set)
        print len(self.new_url_set), len(self.url_set), len(new_urls)
        for new_url in new_urls:
            print new_url, self.urldict[new_url][0]
            # urldict.get(new_url, 'not found')

        self.url_set = copy.deepcopy(self.new_url_set)
        self.new_url_set.clear()
        self.urldict.clear()

def addUrl(urldict, url, title):
    urldict.setdefault(url, []).append(title)
def main():

    urldict = {}
    a_set = set()
    url_set = set()
    new_a_set = set()
    new_url_set = set()


    while(1):
        print "time.ctime() : %s" % time.ctime()

        req = urllib2.Request("http://money.163.com/")
        req.add_header('Cache-Control', 'max-age=0')
        resp = urllib2.urlopen(req)
        # content = resp.read()

        soup = BeautifulSoup(resp.read(), "lxml")

        new_a_set = soup.find_all(href=re.compile("163.com"),text=True)
        for a in new_a_set:

            new_url_set.add(a["href"])
            addUrl(urldict, a["href"], a.string)

        new_urls = new_url_set.difference(url_set)
        print len(new_url_set),len(url_set),len(new_urls)
        for new_url in new_urls:
            print new_url, urldict[new_url][0]
            # urldict.get(new_url, 'not found')

        url_set = copy.deepcopy(new_url_set)
        new_url_set.clear()
        urldict.clear()

        sleep(200)


if __name__ == '__main__':
    main()