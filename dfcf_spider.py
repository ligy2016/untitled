#coding=utf-8
from time import sleep, ctime
from bs4 import BeautifulSoup
import urllib2
import re
import time
import os
import savemd
class kws():
    def __init__(self, domains, kw,start_url):
        self.domains = domains
        self.kw = kw
        self.url = start_url
        self.seen = set()#已经找过的链接
        self.q = set()
    #解析当前页面
    def parse_page(self,url):
        attempts = 0
        success = False

        req = urllib2.Request(url)
        req.add_header('Cache-Control', 'max-age=0')
        req.add_header("User-Agent",
                      "Mozilla/5.0 (X11; Linux x86_6) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.160 Safari/537.22")

        while attempts < 3 and not success:
            try:
                resp = urllib2.urlopen(req, timeout=10)
                self.soup = BeautifulSoup(resp.read(), "lxml")
                resp.close()
                success = True
            except StandardError, e:
                # return 1 #忽略超时等其他错误
                print 'except 34:', e
                attempts += 1
                if attempts == 3:
                    os._exit(0)

    #获取正文部分,仅限东方财富
    def get_content(self,url):
        self.parse_page(url)
        # print self.soup.find_all('p')
        t = self.soup.find(class_='time').text
        context = re.sub(r'''<[^>]+>''', '', str(self.soup.find(id='ContentBody')))
        print t,context
        return (t,context)

    def downloadImg(html):
        reg = r'src="(.+?\.jpg)" pic_ext'
        imgre = re.compile(reg)
        imglist = re.findall(imgre, html)
        # 定义文件夹的名字
        t = time.localtime(time.time())
        foldername = str(t.__getattribute__("tm_year")) + "-" + str(t.__getattribute__("tm_mon")) + "-" + str(
            t.__getattribute__("tm_mday"))
        picpath = 'D:\\ImageDownload\\%s' % (foldername)  # 下载到的本地目录

        if not os.path.exists(picpath):  # 路径不存在时创建一个
            os.makedirs(picpath)
        x = 0
        for imgurl in imglist:
            target = picpath + '\\%s.jpg' % x
            print 'Downloading image to location: ' + target + '\nurl=' + imgurl
            image = urllib.urlretrieve(imgurl, target,  schedule)
            x += 1
        return image;

    #找到页面的所有的链接
    def find_all_links(self,url):
        self.parse_page(url)
        # for s in self.domains:
        div = self.soup.find(id = 'newsListContent')
        all_links = div.find_all(href=True, text = True)

        m = savemd.MD(dbname='test', collname='test')

        if len(self.kw )>0:  #标题关键字查找
            for l in all_links:
                if l["href"] not in self.seen:
                    for kw in self.kw:
                        if kw in l.string:
                            print l["href"],l.string
                            t,context = self.get_content(url=l["href"])
                            doc = {"链接": l["href"], "标题": l.string, "时间": t, "正文": context}
                            m.insert_one_doc(doc=doc)
                            self.seen.add(l["href"])
                            break
        else:#查找所有 不需要匹配关键字
            for l in all_links:
                if l["href"] not in self.seen:
                    print l["href"], l.string
                    t, context = self.get_content(url=l["href"])
                    doc = {"链接": l["href"], "标题": l.string, "时间": t, "正文": context}
                    m.insert_one_doc(doc=doc)
                    self.seen.add(l["href"])
        return

    # 找到前n页的链接，以东方财富http://finance.eastmoney.com/yaowen_cgjjj.html为起始链接
    def read_n_pages(self,n):
        self.find_all_links(url=self.url)
        url = self.url
        for i in range(2,n,1):
            temp = url.replace('.html', '_'+str(i)+'.html')
            # next_url = self.url
            print temp
            self.find_all_links(temp)
            sleep(1)

    def read_next_pages(self,url):
        try:
            div = self.soup.find(id="pagerNoDiv",recursive=True)
            next_page = div.find(href=True,recursive=True, text=u'下一页')
        except StandardError, e:
            print 'except 85:', e
            return

        print next_page["href"]
        index = url.rfind('/')

        next = url[0:index] +'/'+ next_page["href"]
        print next
        sleep(1)
        if next :
            self.find_all_links(url = next)
            # self.url = next
            self.read_next_pages(url=next)
        else:
            return #到最后一页了

class baidu_search(kws):
    def find_all_links(self, url):
        self.parse_page(url)
        for i in range(1,11,1):
            all_links = self.soup.find('table',id = str(i))
            print re.sub(r'''<[^>]+>''', '', str(all_links.find('a'))),re.sub(r'''<[^>]+>''', '', str(all_links.find('font')))

        return
class tianya_search(kws):
    def get_content(self, url):
        self.parse_page(url)
        # print self.soup.find_all('p')
        items = self.soup.find_all(class_='atl-item')
        for item in items:
            item.find(class_='atl-info')
            print t

        # context = re.sub(r'''<[^>]+>''', '', str(self.soup.find(id='ContentBody')))

        # return (t, context)

def main():

    # k = kws(domains=[],kw=[],start_url = 'http://forex.eastmoney.com/news/cdhgd.html')
    # while (1):
    #     k.find_all_links(url=k.url)
    #     sleep(120)

    ty = tianya_search(domains=[],kw=[],start_url = 'http://bbs.tianya.cn/post-develop-2106433-425.shtml#fabu_anchor')
    ty.get_content(url=ty.url)




    # bd = baidu_search(domains=[], kw=[], start_url \
    #    = 'https://www.baidu.com/s?tn=baidurt&rtt=1&bsst=1&cl=3&ie=utf-8&bs=%E6%AC%A7%E6%B4%B2%E5%A4%AE%E8%A1%8C&f=8&rsv_bp=1&wd=%E8%8B%B1%E5%9B%BD%E5%A4%AE%E8%A1%8C&inputT=4700')
    # bd.find_all_links(url = bd.url)

if __name__ == '__main__':
    main()