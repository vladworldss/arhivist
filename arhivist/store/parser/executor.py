# coding: utf-8
"""
Module for composite PoolExecutor and tasks.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from time import time

from .api.google import Api
from .local import book_raw_data

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class Executor(object):

    def __init__(self, max_workers, task, callback=None, *args):

        self.__task = None
        self.__args = []
        self.__callback = None
        self.__futures = []
        self.__ex = ThreadPoolExecutor(max_workers=max_workers)

        # set task
        if callable(task):
            self.__task = task
        else:
            raise TypeError('Task object must be callable')

        # set args for task
        self.__args = args

        # make futures
        self.__futures = tuple(map(lambda x: self.__ex.submit(*x), ((self.__task, x) for x in self.__args)))

        # set callback

        if callable(callback):
            for f in self.__futures:
                f.add_done_callback(callback)

    def execute(self):
        if not self.__task:
            raise Exception("Tasks does't exist")

        waitable = as_completed
        if not self.__callback:
            waitable = wait

        for f in as_completed(self.__futures):
            f.result()
