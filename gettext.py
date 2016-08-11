#coding=utf-8
#!/usr/bin/python

from bs4 import BeautifulSoup
from urllib import urlopen ,urlcleanup
import urllib2
import sys
import re
import time
import copy
import jieba
import jieba.analyse

class PageText():
    def __init__(self,url):
        self.url = url

        self.soup = BeautifulSoup( "lxml")

    def GetSiteContent(self):
        req = urllib2.Request(self.url)
        req.add_header('Cache-Control', 'max-age=0')
        try:
            resp = urllib2.urlopen(req, timeout=10)
        except:
            return 1  # 忽略超时等其他错误
        self.soup = BeautifulSoup(resp.read(), "lxml")
        self.text =  self.gettextonly(soup = self.soup)
        resp.close()
    def gettextonly(self,soup):
        v = soup.string
        if v == None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()
def remove_empty_line(content):
    """remove multi space """
    r = re.compile(r'''^\s+$''', re.M | re.S)
    s = r.sub('', content)
    r = re.compile(r'''\n+''', re.M | re.S)
    s = r.sub('\n', s)
    return s
def remove_jiankuohao(text):
    r = re.compile(r'''<[^>]+>''')
    t = r.findall(text)
    print t
    for n in t :
        print len(n)
    return


def compute_density_thisline(line):
    """Calculate the density for each line, and the average."""
    taglen = 0.0

    r = re.compile(r'''<[^>]+>''')
    t = r.findall(line)
    # print t
    for n in t:
        # print len(n)
        taglen += len(n)
    # print "line total len :%s" % len(line)
    if len(line) > 0:
        # 换行符也站一位算入taglen
        return 1 - (taglen+1)/len(line)
    else:
        return 0


def get_filter_lines(str):
    lines = []
    # with open('d:/1.txt') as file:
    for line in str:
        # do_things(line)
        if compute_density_thisline(line) > 0.5:
                line = remove_any_tag(line)
                lines.append(line)
    return  lines
def save_html(html):
    f_new = file('d:/html.txt', 'w+')
    f_new.write(html)
def write_file_new(data):
    # f = open('d:/1.txt', 'r')
    # data = [line.strip() for line in f.readlines()]
    # data = [line for line in f.readlines()]
    # data = get_filter_lines()
    # f.close()
    f_new = file('d:/output.txt', 'w+')
    # f_new.write(line)
    f_new.writelines(data)
def remove_any_tag (s):
    s = re.sub(r'''<[^>]+>''','',s)

    # return s.strip()
    return s


def OpenUrl(url):
    req = urllib2.Request(url)
    req.add_header('Cache-Control', 'max-age=0')
    try:
        resp = urllib2.urlopen(req, timeout=10)
    except:
        return 1  # 忽略超时等其他错误
    soup = BeautifulSoup(resp.read(), "lxml")
    # print soup.prettify()
    # resp.close()
    resp.urlretrieve(url, r"d:\temp\1.html")
    for eachLine in resp:
# return resp



def main():
    # pt = PageText(url="http://news.163.com/16/0726/01/BSS4GHRK00014JB6.html")
    # pt.GetSiteContent()
    # ct = pt.gettextonly(soup = self.soup)
    # print ct


    # seg_list = jieba.cut(text, cut_all=True)
    # print u"[全模式]: ", "/ ".join(seg_list)
    # text = pt.text
    # tags = jieba.analyse.extract_tags(text, topK=8)

    # print ",".join(tags)
    # print remove_empty_line(text)
    # remove_jiankuohao(text)

    # eachline()
    # compute_density(text)
    str = OpenUrl("http://news.sina.com.cn/c/2016-08-03/doc-ifxuszpp2792303.shtml")
    print str
    # save_html(str)
    # data = get_filter_lines(str)
    # print type(data)
    # write_file_new(data)
if __name__ == '__main__':
    main()