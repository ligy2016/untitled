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

    #判断新的连接是否在指定域内
    def isindomain(self,link):
        for domain in self.domains:
            print domain,link
            # print link
            if domain in link:
                return True
        return False
    #
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