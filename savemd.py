#coding=utf-8
import pymongo
class MD:
    def __init__(self, dbname,collname):
        # self.db = self.get_db()
        self.db = pymongo.MongoClient(host="localhost", port=27017)[dbname]
        self.col = self.db[collname]
    def insert_one_doc(self,doc):
        # 插入一个document
        information_id = self.col.insert(doc)
    def show_doc(self):
        # db.Account.find_one()
        for item in self.col.find():
            print str(item).decode("unicode_escape")

def main():
    m = MD(dbname='test',collname='test')
    # m.insert_one_doc()
    m.show_doc()
if __name__ == '__main__':
    main()