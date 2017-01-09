#coding=utf-8
#!/usr/bin/python
import pymysql
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

    def SelectTopNUrls(self,tablename,n):
        sqlstr = "select url from `%s`.`%s` order by time desc limit 0, %d " % (self.db,tablename, n)
        self.cur.execute(sqlstr)
        return self.cur.fetchall()

    def SaveContent(self, tablename, url, title):
        sqlstr = "select url from `%s`.`%s` where url = '%s'" % (self.db, tablename, url)
        list = self.ExecQuery(sql=sqlstr)
        if len(list) > 0:
            print url, '已存在'
            return
        sqlstr = "insert into `%s`.`%s` (`time`,`title`,`url`) values (now() ,'%s','%s')" % (self.db,tablename, title.strip(),url)
        self.cur.execute(sqlstr)
        # self.conn.commit()

    def SaveUrls(self, tablename, urls, dict):
        if urls is None:
            return
        else:
            for url in urls:
                sqlstr = "select url from `%s`.`%s` where url = '%s'" % (self.db, tablename,url)
                list = self.ExecQuery(sql=sqlstr)
                if len(list)>0:
                    print url,'已存在'
                    continue
                self.SaveContent(tablename, url, dict.get(url, 'not found')[0].strip())

    def InsertContent(self, tablename, content_time ,  title ,	content ,  url ):
        sqlstr = "insert into `%s`.`%s` (`time`,`title`,`url`,`content_time`,`content`) values (now() ,'%s','%s','%s','%s')"\
                 % (self.db,tablename, title.strip(),url,content_time.strip(),content)
        # print sqlstr
        self.cur.execute(sqlstr)

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
        self.cur.execute(sql)
        resList = self.cur.fetchall()

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
        # self.conn.commit()
        # self.conn.close()
