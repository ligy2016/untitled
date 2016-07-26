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

def main ():

    # pt = PageText(url="http://blog.sina.com.cn/s/blog_7d8326290102vzpb.html")
    # pt.GetSiteContent()
    # ct = pt.gettextonly(soup = self.soup)
    # print ct
    text = "中国网7月26日讯 7月23日下午，北京延庆区八达岭野生动物园发生一起老虎咬人事件，造成一死一重伤。据延庆区委宣传部通报，事故发生在当事游客自驾游过程中，游客私自下车后受到老虎攻击。目前，北京警方正在调查此事，涉事动物园已被停业整顿，配合调查。\
            据悉，事发于园内猛兽区东北虎园，根据当日监控视频显示，在自驾游车道上，一年轻女子从轿车副驾驶下车走到驾驶员一边，驾驶员打开车门，两人开始对话，突然，一只老虎猛地向该女子身后扑来，女子回头的瞬间被老虎咬住并迅速向后拖拽，驾驶员见状下车营救，随后后座一位女子也冲下车子营救。\
            据了解，目前，受重伤的年轻女子已脱离生命危险，但仍不能排除感染的可能。下车营救的女子是其母，不幸的是，这位母亲当场被另外一只老虎扑咬致死。\
            中国政法大学传播法研究中心副主任朱巍在接受中国网记者采访时表示，在我国，以前对于动物园造成他人损害的侵权责任存在一定争议。2009年，《中华人民共和国侵权责任法》出台，特别把这种情况进行了明文规定。\
            该法第十章为饲养动物损害责任，其中第八十一条规定，动物园的动物造成他人损害的，动物园应当承担侵权责任，但能够证明尽到管理职责的，不承担责任。\
            “从这条规定来看，动物园动物造成他人损害的，承担的是过错推定责任，先推定动物园有责任，但如果能证明自己完成安全保障义务和管理职责的话，就不用担责。”朱巍说。\
            据悉，在八达岭野生动物园，自驾游的游客入园前都要签订《自驾车入园游览车损责任协议书》，记者看到，该协议第一条即写明“猛兽区必须关好、锁好车门、车窗，禁止投喂食物、严禁下车”；同时规定“如因违反上述规定发生的车辆损伤和人员伤害，自驾车主应负相应的责任”。\
            此外，景区内有相关的安全提示牌，并有巡逻车来回巡视，还有广播反复提醒游客安全注意事项，也包括禁止下车。\
            监控视频显示，年轻女子被咬后，附近一辆墨绿色吉普车立即驶向老虎拖拽方向。延庆区园林绿化局新闻发言人王淑琴表示，该车就是园区的安全保障巡逻车，“她下车之前，巡逻车还用喇叭喊，让她别下来，她还是下来了。”"
    # seg_list = jieba.cut(text, cut_all=True)
    # print u"[全模式]: ", "/ ".join(seg_list)

    tags = jieba.analyse.extract_tags(text, topK=10)

    print ",".join(tags)
if __name__ == '__main__':
    main()