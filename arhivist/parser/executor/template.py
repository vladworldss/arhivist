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

    def callback(self):
        raise NotImplementedError
