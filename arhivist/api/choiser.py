# coding: utf-8
"""
Classes for choise, compare values.
"""
from difflib import SequenceMatcher

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class Choiser(object):
    """
    Choiser class.
    """

    @staticmethod
    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    @classmethod
    def best_choise(cls, raw_value, resp_values):
        compare = map(lambda x: (x, cls.similar(raw_value, x), resp_values))
        sorted_titles = sorted(compare, key=lambda pair: pair[1])
        return sorted_titles[-1][0]
