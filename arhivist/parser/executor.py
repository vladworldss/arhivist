# coding: utf-8
from importlib import import_module
import os
from pprint import pprint
import json
import requests
from requests.auth import HTTPBasicAuth
from concurrent.futures import ThreadPoolExecutor
import api
from settings import POST_URL


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
                    resp = requests.post(url=POST_URL, data=r, auth=HTTPBasicAuth('admin', 'password123'))
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
