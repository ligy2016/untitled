#coding=utf-8
import pymongo

def get_db():
    # 建立连接
    client = pymongo.MongoClient(host="localhost", port=27017)
    db = client['example']
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
    information = {"name": "quyang", "age": "25"}
    information_id = coll.insert(information)
    print information_id
def main():
    db = get_db()
    insert_one_doc(db)

if __name__ == '__main__':
    main()