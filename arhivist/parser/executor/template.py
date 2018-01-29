# coding: utf-8
"""
Module of Abstract Executor classes.
"""
import abc

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class AbsExecutor(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def execute(self, *args, **kw):
        pass

    @abc.abstractmethod
    def task(self):
        pass

    @abc.abstractmethod
    def callback(self):
        pass


class BaseExecutor(AbsExecutor):

    ApiCls = type

    def __init__(self, api):
        if not isinstance(api, self.ApiCls):
            raise TypeError("This is not supported ApiCls")
        self.api = api
