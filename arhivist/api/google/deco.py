# coding: utf-8
"""
Decorators for Google API.
"""
from functools import wraps

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"

_volumeInfo = {"publisher", "description", "language"}


def parse_responce(resp_json):
    if not isinstance(resp_json, dict):
        raise TypeError
    data = {}
    volumeInfo = resp_json.pop("volumeInfo", None)
    if volumeInfo:
        for key in _volumeInfo:
            data[key] = volumeInfo.pop(key, "")

        data["description"] = data.pop("description", "")[:1024]
        data["published_date"] = volumeInfo.pop("publishedDate", "")
        data["title"] = volumeInfo.pop("title", "")
        data["page_count"] = volumeInfo.pop("pageCount", 0)
        data["volume_link"] = volumeInfo.pop("canonicalVolumeLink", "")
        data["thumbnail"] = {
            "volume_link": volumeInfo.get("imageLinks", {}).get("thumbnail", ""),
            "name": "",
        }

        identifiers = resp_json.pop("volumeInfo", None)
        if identifiers:
            for id in identifiers:
                _id = id["identifier"]
                if len(_id) == 10:
                    data["isbn_10"] = _id
                elif len(_id) == 13:
                    data["isbn_13"] = _id
                else:
                    raise Exception

        data["author"] = volumeInfo.pop("author", "")
        data["category"] = volumeInfo.pop("category", "")
    return data


def parsed(func):
    @wraps(func)
    def wrapper(*args, **kw):
        res = func(*args, **kw)
        if res:
            items = res.get("items")
            if items:
                res = [parse_responce(x) for x in items]
        return res
    return wrapper
