# coding: utf-8
"""
Module of the Book class.
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


class Book(object):

    __BOOK_NAME_MASK = re.compile(r'(?P<name>\w+)\.(?P<type>\w+)')

    __SUPPORTED = SUPPORT_BOOK_EXTENSION

    __slots__ = ("publisher", "description", "language", "published_date",
                 "title", "page_count", "canonical_volume_link", "isbn_10",
                 "isbn_13", "author", "category", "thumbnail", "path", "raw_title",
                 "file_ext"
                 )

    def __init__(self, raw_title, path, file_ext):
        for attr in self.__slots__:
            setattr(self, attr, None)

        self.raw_title = raw_title
        self.path = path
        self.file_ext = file_ext

    def to_json(self):
        """
        Convert self-instance to json-str.

        :return:
        """
        raise NotImplementedError

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
                book_name = " ".join(m)
                return (book_name, book_type)
