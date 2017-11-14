# coding: utf-8
from importlib import import_module
from pprint import pprint
import requests
from requests.auth import HTTPBasicAuth
from concurrent.futures import ThreadPoolExecutor
from .api.google import Book

from .settings import POST_URL, CREDENTIALS, THUMBNAIL_DIR

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class BookExecutor(object):

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
                    resp = requests.post(url=POST_URL, data=r, auth=HTTPBasicAuth(*CREDENTIALS))
                    pprint(f'resp: {resp.content}')

    @classmethod
    def Api(cls, vendor):
        # _module = import_module('api.{}'.format(vendor))
        # BookApiCls = getattr(_module, 'Book')
        # return BookApiCls(download_dir=THUMBNAIL_DIR)
        return Book(download_dir=THUMBNAIL_DIR)

    @classmethod
    def execute(cls, items, api_vendor, callback=True):
        Api = cls.Api(api_vendor)
        with ThreadPoolExecutor(max_workers=1) as ex:
            for item in items:
                f = ex.submit(cls.task, item, Api)
                f.arg = item
                if callback:
                    f.add_done_callback(cls.callback)
