#coding=utf-8
import pymongo

def get_db():
    # 建立连接
    client = pymongo.MongoClient(host="localhost", port=27017)
    db = client['test']
    #或者 db = client.example
    return db
def get_collection(db):
    # 选择集合（mongo中collection和database都是延时创建的）
    coll = db['test']
    print db.collection_names()
    return coll
def insert_one_doc(db):
    # 插入一个document
    coll = db['test']
    information = {"name": u"肖明", "age": "25","sex":"male"}
    information_id = coll.insert(information)
    print information_id
def show_doc(db):
    account = db.Account
    # db.Account.find_one()
    for item in db.test.find():
        print str(item)

def main():
    db = get_db()
    insert_one_doc(db)
    show_doc(db)
if __name__ == '__main__':
    main()