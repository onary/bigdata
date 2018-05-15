from pymongo import ASCENDING
from settings import DB


def save(insert, update):
    if len(insert):
        result = DB.products.insert_many(insert)

    for item in update:
        query = {'$addToSet': {}, '$set': {}}
        for k,v in item.items():
            if type(v) == list:
                query['$addToSet'][k] = {'$each': v}
            else:
                query['$set'][k] = v

        if query['$addToSet'] == {}:
            del query['$addToSet']

        result = DB.products.update_one({'uid': item['uid']}, query)


def get_revisions():
    products = DB.products
    if products.count() > 0:
        return dict([(i['uid'], i['revisions']) for i in \
            products.find({}, {'uid': 1, 'revisions': 1, '_id': 0})])
    else:
        return {}


def drop_table():
    DB.products.drop()


def create_index():
    DB.products.create_index([('uid', ASCENDING)], unique=True)


if __name__ == "__main__":
    drop_table()
    create_index()