import pymongo


class MongoUtil(object):
    client: pymongo.MongoClient
    db: None
    collection: None

    def __init__(self, **kwargs):
        if not kwargs == []:
            if "ip" in kwargs and "port" in kwargs:
                self.connect(kwargs["ip"], kwargs["port"])
                if "db" in kwargs:
                    self.use_db(kwargs["db"])

    def connect(self, ip='localhost', port=27017):
        self.client = pymongo.MongoClient("mongodb://{}:{}/".format(ip, str(port)))

    def use_db(self, db):
        self.db = self.client[str(db)]
        return self.db

    def use_table(self, name):
        self.collection = self.db[name]
        return self.collection

    def dbs(self):
        print(self.client.list_database_names())

    def exist_db(self, db):
        db_list = self.client.list_database_names()
        # insert data successfully as create database clear
        return db in db_list

    def show(self):
        for x in self.collection.find():
            print(x)
        return self

    def find(self, d_dict):
        arr = []
        for x in self.collection.find(d_dict):
            arr.append(x)
        return arr

    def insert(self, data):
        self.collection.insert_one(data)
        return self

    def clear(self):
        self.collection.delete_many({})
        return self

    def drop(self):
        self.collection.drop()

    def search(self, condition):
        conditions = {}
        for (k, v) in condition.items():
            conditions[k] = {'$regex': v}
        return self.collection.find(conditions)


if __name__ == '__main__':
    mu = MongoUtil()
    mu.connect()
    mu.use_db('test')
    mu.use_table('output0.ts')
    print(mu.find({
        "result": False,
        "url": "",
    }))
