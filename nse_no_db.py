#coding=utf-8
#!/usr/bin/python
import pymysql
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
class ScrawlSite():
    def __init__(self,url,tablename):
        self.url = url
        self.tablename = tablename
        self.urldict = {}
        self.a_set = set()
        self.url_set = set()
        self.new_a_set = set()
        self.new_url_set = set()
        self.soup = BeautifulSoup( "lxml")

    def GetSiteContent(self):
        req = urllib2.Request("http://money.163.com/")
        req.add_header('Cache-Control', 'max-age=0')
        resp = urllib2.urlopen(req)
        self.soup = BeautifulSoup(resp.read(), "lxml")

    def FindPattern(self):
        self.new_a_set = self.soup.find_all(href=re.compile("163.com"), text=True)
        pass
    def GetNewLinks(self):
        for a in self.new_a_set:
            self.new_url_set.add(a["href"])
            # self.addUrl(urldict, a["href"], a.string)
            self.urldict.setdefault(a["href"], []).append(a.string)
        self.new_urls = self.new_url_set.difference(self.url_set)
        return self.tablename,self.new_urls,self.urldict

        # print len(self.new_url_set), len(self.url_set), len(self.new_urls)
        # for new_url in new_urls:
        #     print new_url, self.urldict[new_url][0]

    def UpdateSet(self):
        self.url_set = copy.deepcopy(self.new_url_set)
        self.new_url_set.clear()
        self.urldict.clear()
        self.new_urls.clear()
class SS_163(ScrawlSite):
    def FindPattern(self):
        self.new_a_set = self.soup.find_all(href=re.compile("163.com"), text=True)
class MYSQL:
    """
    对pymysql的简单封装
    """
    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymysql.connect(host=self.host,user=self.user,passwd=self.pwd,db=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur
    def SaveContent(self, tablename, url, title):
        sqlstr = "insert into `db_1`.`%s` (`url`, `title`,`date`) values ('%s','%s',now() )" % (tablename,url, title.strip())
        self.cur.execute(sqlstr)
        self.conn.commit()


    def ExecQuery(self,sql):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段

        调用示例：
                ms = MYSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
                resList = ms.ExecQuery("SELECT id,NickName FROM WeiBoUser")
                for (id,NickName) in resList:
                    print str(id),NickName
        """
        # cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        #查询完毕后必须关闭连接
        # self.conn.close()
        return resList
    def ConnectDB(self):
        self.cur = self.__GetConnect()
    def DisconnectDB(self):
        self.conn.close()


    def ExecNonQuery(self,sql):
        """
        执行非查询语句

        调用示例：
            cur = self.__GetConnect()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        """
        # cur = self.__GetConnect()
        self.cur.execute(sql)
        self.conn.commit()
        # self.conn.close()


# def addUrl(urldict, url, title):
#     urldict.setdefault(url, []).append(title)
def main():
    mysql = MYSQL(host="127.0.0.1", user="root", pwd="123456", db="db_1")
    ss = SS_163(url = "http://money.163.com/",tablename = "urls_163")


    mysql.ConnectDB()

    while(1):
        print "time.ctime() : %s" % time.ctime()
        ss.GetSiteContent()
        ss.FindPattern()
        (tablename,urls,dict) = ss.GetNewLinks()
        for url in urls:
            mysql.SaveContent(tablename,url,dict.get(url, 'not found')[0].strip())
        ss.UpdateSet()
        sleep(120)

    mysql.DisconnectDB()


if __name__ == '__main__':
    main()