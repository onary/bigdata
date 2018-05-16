import argparse
from pymongo import ASCENDING
from settings import DB


def save(db, insert, update):
    if len(insert):
        result = db.products.insert_many(insert)

    for item in update:
        query = {'$addToSet': {}, '$set': {}}
        for k,v in item.items():
            if type(v) == list:
                query['$addToSet'][k] = {'$each': v}
            else:
                query['$set'][k] = v

        if query['$addToSet'] == {}:
            del query['$addToSet']

        result = db.products.update_one({'uid': item['uid']}, query)


def get_revisions(db):
    products = db.products
    if products.count() > 0:
        return dict([(i['uid'], i['revisions']) for i in \
            products.find({}, {'uid': 1, 'revisions': 1, '_id': 0})])
    else:
        return {}


def drop_table(db):
    db.products.drop()


def create_index(db):
    db.products.create_index([('uid', ASCENDING)], unique=True)


# You can use this script for clearing DB and creating indexes
# python db.py 1      - testing DataBase
# python db.py 0      - production DataBase
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("debug")
    args = parser.parse_args()

    arg = False if args.debug in ['0', 0, 'False', 'false', ''] else True
    drop_table(DB(arg))
    create_index(DB(arg))