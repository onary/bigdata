from collections import defaultdict, OrderedDict
from hashlib import sha1


def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v
                     for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v)
                        for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d


def dict_deep_access(dd, path):
    if type(path) == int:
        return dd[path]
    elif type(path) == list:
        return tuple(dict_deep_access(dd, path[0]).split(','))

    val = dd
    for key in path.split('.'):
        val = val.get(key, None)
    return val


def parse_row(fields, row):
    result = OrderedDict()
    for k,v in fields.items():
        if v != None:
            v = dict_deep_access(row, v)
            if v != None:
                result[k] = v

    return result


def hash_from_dict(dd):
    return sha1(
        "|".join(
            map(
                lambda i: ('{0}:{1}'.format(i[0],i[1]) or '').strip(),
                dd.items()
            )
        ).encode("utf8")
    ).hexdigest()
