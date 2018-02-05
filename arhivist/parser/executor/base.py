# coding: utf-8
"""
Module of Base Executor classes.
"""
import os
from importlib import import_module
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import wraps
from collections import defaultdict

from .template import AbsExecutor

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class BaseExecutor(AbsExecutor):

    def __init__(self, task_api, callback_api=None):
        self.task_api = task_api
        self.callback_api = callback_api


class PoolExecutor(BaseExecutor):

    __ExecCls = ThreadPoolExecutor

    def execute(self, items, **kw):
        with self.__ExecCls(max_workers=kw.get("max_workers", os.cpu_count())) as ex:
            wait_for = []
            for item in items:
                f = ex.submit(self.task, item)
                f.arg = item
                if kw.get("callback", False):
                    f.add_done_callback(self.callback)
                wait_for.append(f)

            results = defaultdict(list)
            for f in as_completed(wait_for):
                try:
                    book = f.result()
                    if book._bad:
                        results["bad"].append(book)
                    else:
                        results["ok"].append(book)
                except:
                    results["bad"].append(f.arg)
            return results


def init_api(meth):
    @wraps(meth)
    def foo(cls, vendor=None, *args, **kw):
        vendor_api = None
        if vendor:
            vendor_api = cls.VendorApi(vendor)(*args, **kw)
        kw["vendor_api"] = vendor_api
        kw["arhivist_api"] = cls.ArhivistApi()
        return meth(cls, vendor, *args, **kw)

    return foo


class ExecutorFactory(object):

    __ApiPath = "arhivist.api"
    __ArhivistApi = None
    ItemType = None

    # __Private
    @classmethod
    def __api_module(cls, vendor):
        return import_module('{}.{}'.format(cls.__ApiPath, vendor))

    # __Public
    @classmethod
    def VendorApi(cls, vendor):
        _m = cls.__api_module(vendor)
        return getattr(_m, cls.ItemType)

    @classmethod
    def ArhivistApi(cls):
        if not cls.__ArhivistApi:
            cls.__ArhivistApi = cls.VendorApi("client")()
        return cls.__ArhivistApi

    @classmethod
    def make_init_executor(cls, vendor, *args, **kw):
        raise NotImplementedError

    @classmethod
    def make_update_executor(cls, vendor, *args, **kw):
        raise NotImplementedError

    @classmethod
    def make_delete_executor(cls, *args, **kw):
        raise NotImplementedError
