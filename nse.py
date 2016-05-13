#coding=utf-8
#!/usr/bin/python

import pymysql
from time import sleep, ctime
from bs4 import BeautifulSoup
from urllib import urlopen
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

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
 self.c pymysql.connect(host=self.host,user=self.user,passwd=self.pwd,db=self.db,charset="utf8")
 cur = self.conn.cursor()
 if not cur:
 raise(NameError,"连接数据库失败")
 else:
 return cur

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

def addUrl(urldict, url, title):
 urldict.setdefault(url, []).append(title)
def main():

 urldict = {}
 a_set = set()
 url_set = set()
 new_a_set = set()
 new_url_set = set()

 mysql = MYSQL(host="127.0.0.1",user="root",pwd="123456",db="db_1")

 mysql.ConnectDB()
 while(1):
 html = urlopen("http://wallstreetcn.com/")
 soup = BeautifulSoup(html.read(), "lxml")
 # links = bsobj.find_all('a', class_='title')
 # links = bsobj.find_all('a')
 new_a_set = soup.find_all(class_=re.compile("title"),href=re.compile("com"))
 for a in new_a_set:
 # print a.string.strip(),a["href"]
 new_url_set.add(a["href"])
 addUrl(urldict, a["href"], a.string)

 new_urls = new_url_set.difference(url_set)

 for new_url in new_urls:
 print new_url, urldict[new_url][0], urldict.get(new_url, 'not found')
 sqlstr = "insert into `db_1`.`urls_163` (`url`, `title`,`date`) values ('%s','%s',now() )" % (new_url, urldict.get(new_url, 'not found')[0])
 mysql.ExecNonQuery(sqlstr)
 '''for eachlink in links:
 # href = [v for k, v in eachlink.attrs.iteritems() if k == 'href']
 # if href:
 #     title = eachlink.get_text().strip()
 #     h = href

 # sqlstr = "insert into `db_1`.`urls_163` (`url`, `title`,`time`) values (%s,%s,now() )",(eachlink.attrs['href'] ,eachlink.get_text().strip())
 sqlstr = "insert into `db_1`.`urls_163` (`url`, `title`,`date`) values ('%s','%s',now() )"%(eachlink.attrs['href'],eachlink.get_text().strip())
 # print mysql
 mysql.ExecNonQuery(sqlstr)'''

 url_set = new_url_set
 new_url_set.clear()
 urldict.clear()

 sleep(120)
 mysql.DisconnectDB()

if __name__ == '__main__':
 main()
