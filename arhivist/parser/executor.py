# coding: utf-8
from importlib import import_module
from pprint import pprint
import requests
from requests.auth import HTTPBasicAuth
from concurrent.futures import ThreadPoolExecutor

from settings import POST_URL, CREDENTIALS

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class BookExecutor(object):

    @staticmethod
    def task(item, Api):
        title = item.get('raw_title', '')
        resp = Api.title_list(title, maxResults=1)
        item_set = set(item)
        result = []

        # через map
        for r in resp:
            _chain = {}
            if not (item_set & set(r)) == set():
                raise Exception
            _chain.update(**item)
            _chain.update(**r)
            result.append(_chain)

        return result

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
        _module = import_module('api.{}'.format(vendor))
        return getattr(_module, 'Book')()

    @classmethod
    def execute(cls, items, api_vendor):
        Api = cls.Api(api_vendor)
        with ThreadPoolExecutor(max_workers=1) as ex:
            for item in items:
                f = ex.submit(cls.task, item, Api)
                f.arg = item
                f.add_done_callback(cls.callback)
