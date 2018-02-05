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
    def best_choise(cls, value, choises, field, expect_val=0.6):
        """

        :param value: etalon value
        :param list choises: responces
        :param str field: resp attr whose will be based for compare values
        :param float expect_val: minimal value of comparation of matching

        :return: best responce
        """

        try:
            if not choises:
                raise TypeError("Empty choises")
            compare = map(
                lambda x: (x, cls.similar(value, x[field])),
                choises
            )
            resp, rat_value = max(compare, key=lambda pair: pair[1])
            if rat_value >= expect_val:
                return resp
        except Exception as e:
            # debag
            res = value, choises, field
            pass

    @classmethod
    def best_book_choise(cls, value, choises, field="title"):
        return cls.best_choise(value, choises, field)
