from os import path
from pymongo import MongoClient

BASE_DIR = path.dirname(path.abspath(__file__))

DATA_DIR = path.join(BASE_DIR, 'data')

CONFIGS_DIR = path.join(BASE_DIR, 'configs')

MCLIENT = MongoClient('mongodb://localhost:27017/')

DB = MCLIENT.bigdata

CHANK_SIZE = 1000