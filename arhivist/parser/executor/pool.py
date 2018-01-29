# coding: utf-8
"""
Module of PoolExecutor classes.
"""
import os
from concurrent.futures import ThreadPoolExecutor

from .template import BaseExecutor
from arhivist.api.template import AbsBookApi

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class PoolExecutor(object):

    def execute(self, items, **kw):
        with ThreadPoolExecutor(max_workers=kw.get("max_workers", os.cpu_count())) as ex:
            results = []
            for item in items:
                f = ex.submit(self.task, item)
                f.arg = item
                if kw.get("callback", False):
                    f.add_done_callback(self.callback)

                # TODO: return result of callback


class BookExecutor(BaseExecutor, PoolExecutor):

    ApiCls = AbsBookApi


class InitExecutor(BookExecutor):

    def task(self, book):
        resp = self.api.search_book(book.raw_title)
        thum_path = self.api.download_thumbnail()

