# coding: utf-8
"""
Module of Common Arhivist Data Type.
"""
import re
import json

from .settings import SUPPORT_BOOK_EXTENSION

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.2"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class Item(object):
    """
    Base class of supported Store items.
    """
    __slots__ = ()

    def __init__(self):
        for attr in self.__slots__:
            setattr(self, attr, None)

    @classmethod
    def from_json(cls, _json):
        """
        Creating Item instance from json.

        :param str _json: JSON serializable str
        :return:
        """
        dict_fields = json.loads(_json)
        item = cls.__new__(cls)
        item.__init__(**dict_fields)

        item.update(dict_fields)
        return item

    def to_json(self):
        """
        Convert self-instance to JSON serializable str.
        Result has only those attrs whose specified into __slots__.

        :return: JSON serializable str of self
        """

        return json.dumps(self.to_dict())

    def update(self, dict_fields):
        """
        Update item fields from or dict.
        Only attr-fields will be updated.

        :param dict dict_fields:
        :return:
        """

        if not isinstance(dict_fields, dict):
            raise TypeError

        for key, value in dict_fields.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self):
        """
        Creating dict implement of instance.

        :return: dict
        """
        res = {}
        for x in self.__slots__:
            attr = getattr(self, x)
            if isinstance(attr, Item):
                attr = attr.to_dict()
            res[x] = attr
        return res


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
        if self.thumbnail:
            self.thumbnail = Thumbnail(**self.thumbnail)


class Thumbnail(Item):
    """
    Thumbnail class.
    """
    __slots__ = ("name",
                 "volume_link"
                 )

    def __init__(self, name=None, volume_link=None):
        super().__init__()
        self.name = name
        self.volume_link = volume_link
