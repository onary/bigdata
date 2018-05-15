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
    revisions = defaultdict(list, get_revisions())
    insertList = []
    updateList = []

    for row in reader(arg):
        row_hash = hash_from_dict(row)
        uid = row['uid']

        if uid in revisions and row_hash in revisions[uid]:
            continue

        row['revisions'] = [row_hash]

        if uid in revisions:
            updateList.append(row)
        else:
            insertList.append(row)

        revisions[uid].append(row_hash)

        if CHANK_SIZE in [len(insertList), len(updateList)]:
            save(insertList, updateList)
            insertList.clear()
            updateList.clear()

    save(insertList, updateList)


if __name__ == "__main__":
    if args.config:
        parse(args.config)
