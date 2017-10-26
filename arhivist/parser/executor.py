# coding: utf-8
from importlib import import_module
import os
from pprint import pprint
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import api
from settings import POST_URL


class BookExecutor(object):

    @staticmethod
    def task(item, Api):
        res = Api.list(item, maxResults=1)
        return res

    @staticmethod
    def callback(fn):
        if fn.cancelled():
            print('{}: canceled'.format(fn.arg))
        elif fn.done():
            error = fn.exception()
            if error:
                print('{}: error returned: {}'.format(fn.arg, error))
            else:
                result = fn.result()
                for r in result:
                    # if not (set(r) & set(fn.arg)) == set():
                    #     raise Exception
                    # req = r.update({'path': fn.arg['path']})
                    resp = requests.post(url=POST_URL, data=r)
                    pprint(f'resp: {resp.content}')

    @staticmethod
    def execute(items, api_vendor):
        api_module = getattr(api, api_vendor.lower())
        Api = getattr(api_module, 'Book')()

        with ThreadPoolExecutor(max_workers=1) as ex:
            for i in items:
                title = f"intitle:{i['raw_title']}"
                f = ex.submit(BookExecutor.task, title, Api)
                f.arg = i
                f.add_done_callback(BookExecutor.callback)
