# coding: utf-8
"""
Module of Common Arhivist DataType.
"""
import re
import json

from .settings import SUPPORT_BOOK_EXTENSION

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"
__all__        = ("BooksList", "BookDetail", "CategoryList")


class Item(object):
    """
    Base class of supported Store items.
    """
    __slots__ = ()

    def __init__(self):
        for attr in self.__slots__:
            setattr(self, attr, None)

    @staticmethod
    def from_json(_json):
        """
        Create Item instance from json.

        :param _json:
        :return:
        """
        raise NotImplementedError

    def to_json(self):
        """
        Convert self-instance to json-str.
        Result has only those attrs whose specified into __slots__.

        :return: JSON serializable str of self
        """
        res = {}
        for x in self.__slots__:
            attr = getattr(self, x)
            if isinstance(attr, Item):
                attr = attr.to_json()
            res[x] = attr
        return json.dumps(res)

    def update(self, _json):
        """
        Update item fields from json.

        :param str or dict _json:
        :return:
        """
        if isinstance(_json, str):
            _json = json.loads(_json)
        elif not isinstance(_json, dict):
            raise TypeError

        # all keys must be in self.attrs
        if not all(hasattr(self, x) for x in _json):
            raise AttributeError
        for key, value in _json.items():
            setattr(self, key, value)


class Book(Item):
    """
    Book class.
    """

    __BOOK_NAME_MASK = re.compile(r'(?P<name>\w+)\.(?P<type>\w+)')

    __SUPPORTED = SUPPORT_BOOK_EXTENSION

    __slots__ = ("publisher",
                 "description",
                 "language",
                 "published_date",
                 "title",
                 "page_count",
                 "volume_link",
                 "isbn_10",
                 "isbn_13",
                 "author",
                 "category",
                 "thumbnail",
                 "path",
                 "raw_title",
                 "file_ext"
                 )

    def __init__(self, path, raw_title, file_ext):
        super().__init__()
        self.path = path
        self.raw_title = raw_title
        self.file_ext = file_ext

    def get_meta(self):
        """
        Get meta-info of the book from embedded descr.

        :return:
        """
        raise NotImplementedError

    @classmethod
    def __book_name_match(cls, file_name):
        """
        Regex for book-title.

        :param str file_name:
        :return:
        """
        return cls.__BOOK_NAME_MASK.match(file_name)

    @staticmethod
    def __unicode_name_match(file_name):
        """
        Regex for unicode-book-title.

        :param str file_name:
        :return:
        """
        return re.findall(r'(?u)[\w\']+', file_name)

    @classmethod
    def match(cls, file_name):
        """
        Determines whether the file is a book. If it's true, return list of attrs

        :param str file_name: filename
        :return: ("title", "file_ext") or None
        """
        if any(file_name.endswith(s) for s in cls.__SUPPORTED):

            # match cyrillic titles
            m = cls.__unicode_name_match(file_name)
            if m:
                book_type = m.pop()
                book_title = " ".join(m)
                return (book_title, book_type)

    def update(self, _json):
        super().update(_json)
        self.thumbnail = Thumbnail(**self.thumbnail)


class Thumbnail(Item):

    __slots__ = ("name",
                 "volume_link"
                 )

    def __init__(self, name=None, volume_link=None):
        super().__init__()
        self.name = name
        self.volume_link = volume_link
