# coding: utf-8
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from functools import wraps

from importlib import import_module
from pprint import pprint
import requests
from concurrent.futures import ThreadPoolExecutor

from settings import *

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class BookExecutor(object):

    def validate(self, raw_titile, resp_title):
        res = False
        raw_set = frozenset(raw_titile.split())
        resp_set = frozenset(resp_title.split())


    @staticmethod
    def task(item, Api, max_results=1):
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

    @classmethod
    def Api(cls, vendor):
        _module = import_module('api.{}'.format(vendor))
        BookApiCls = getattr(_module, 'Book')
        return BookApiCls(download_dir=THUMBNAIL_DIR)

    @classmethod
    def execute(cls, items, api_vendor, callback=True):
        Api = cls.Api(api_vendor)
        with ThreadPoolExecutor(max_workers=1) as ex:
            for item in items:
                f = ex.submit(cls.task, item, Api)
                f.arg = item
                if callback:
                    f.add_done_callback(cls.callback)
