from os.path import join
import xml.etree.ElementTree as etree
import csv
import json

from utils import etree_to_dict, parse_row
import settings


def xml_reader(config, file):
    for event, elem in etree.iterparse(file, events=("start", "end")):
        if event == "end" and elem.tag == config['tag']:
            row = etree_to_dict(elem)[config['tag']]
            elem.clear()
            yield parse_row(config['fields'], row)


def csv_reader(config, file):
    with open(file, "r") as csvfile:
        datareader = csv.reader(csvfile, delimiter=config['delimiter'] or ',')
        for row in datareader:
            if len(row) < config['minRowLength']:
                continue
            else:
                yield parse_row(config['fields'], row)


READER = {
    "csv": csv_reader,
    "xml": xml_reader
}


def config_load(filename):
    path = join(settings.CONFIGS_DIR, '{0}.json'.format(filename))
    with open(path, 'r') as f:
        return json.load(f)


def reader(arg):
    func = READER.get(arg, None)

    if func == None:
        return []

    config = config_load(arg)
    file = join(settings.DATA_DIR, config['path'])

    return func(config, file)