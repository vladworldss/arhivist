# coding: utf-8

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from functools import wraps

from importlib import import_module
from pprint import pprint
import requests

from difflib import SequenceMatcher


from settings import *

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"







class BookExecutor(AbsExecutor):

    def __init__(self, store):
        self.store = store

    @staticmethod
    def validate(raw_tile, resp_titles):

        def similar(a, b):
            return SequenceMatcher(None, a, b).ratio()

        compare = map(lambda x: (x, similar(raw_tile, x), resp_titles))
        sorted_titles = sorted(compare, key=lambda pair: pair[1])
        best_title = sorted_titles[-1][0]
        return best_title

    @staticmethod
    def task(item, Api, max_results=10):
        def update(r):
            if item_set.intersection(set(r)):
                raise Exception
            r.update(**item)

        item_set = set(item)
        resp = Api.title_list(item['raw_title'], maxResults=max_results)
        for r in resp:
            Api.download_thumbnail(r)
        list(map(update, resp))
        return resp

    @classmethod
    def callback(cls, fn):
        if fn.cancelled():
            print('{}: canceled'.format(fn.arg))
        elif fn.done():
            error = fn.exception()
            if error:
                print('{}: error returned: {}'.format(fn.arg, error))
            else:
                result = fn.result()
                for r in result:
                    resp_json = requests.post(url=AUTH_URL, data=CREDENTIALS).json()
                    token = resp_json["token"]
                    resp = requests.post(url=POST_URL, data=r, headers={'Authorization': f'JWT {token}'})
                    # resp = requests.post(url=POST_URL, data=r, auth=auth)
                    pprint(f'resp: {resp.content}')
