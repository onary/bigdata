from collections import defaultdict
import argparse

from readers import reader
from db import save, get_revisions
from utils import hash_from_dict
from settings import CHANK_SIZE


parser = argparse.ArgumentParser()
parser.add_argument("config")
args = parser.parse_args()


def parse(arg):
    # load revisions from database and store in format
    # {id1: [revision1, revison2], id2: [rev3] ... }
    revisions = defaultdict(list, get_revisions())

    # buffers for accumulating processed data before save
    insertList = []
    updateList = []

    # iterating through generator
    for row in reader(arg):
        uid = row['uid']

        # creating hash from processed record
        # duplicates will have same hash, so we can ignore them
        row_hash = hash_from_dict(row)

        # check if hash in revisions
        if uid in revisions and row_hash in revisions[uid]:
            continue

        # write hash to our record, so we will able to extract in during next parse
        row['revisions'] = [row_hash]

        if uid in revisions:
            updateList.append(row)
        else:
            insertList.append(row)

        # add hash to revision, so we can omit following duplicates of current parse
        revisions[uid].append(row_hash)

        # save data to DB when localstorage reaches chunk size
        if CHANK_SIZE in [len(insertList), len(updateList)]:
            save(insertList, updateList)
            insertList.clear()
            updateList.clear()

    # saving the rest of the data (if any) to DB
    save(insertList, updateList)


if __name__ == "__main__":
    if args.config:
        parse(args.config)
