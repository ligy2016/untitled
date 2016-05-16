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

        req = urllib2.Request("http://wallstreetcn.com/")
        req.add_header('Cache-Control', 'max-age=0')
        resp = urllib2.urlopen(req)
        # content = resp.read()

        soup = BeautifulSoup(resp.read(), "lxml")

        new_a_set = soup.find_all(class_=re.compile("title"),href=re.compile("node"),text=True)
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