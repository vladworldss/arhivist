# coding: utf-8
"""
Module for working with book store.
"""
import os
import sys
sys.path.append(__file__)

import re
import argparse
from collections import OrderedDict

from executor import BookExecutor
import settings as st

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class Store(object):
    """
    Book store class.
    """
    SUPPORT_FILE_EXTENSION = {'pdf', 'djvu', '.djv', 'epub', 'fb2'}
    _BOOK_NAME_MASK = re.compile(r'(?P<name>\w+)\.(?P<type>\w+)')
    REQ_KEYS = ('path', 'raw_title', 'file_ext')

    def __init__(self, root_path=st.STORE_PATH):
        self.root_path = root_path
        self.Executor = BookExecutor

    @staticmethod
    def BOOK_NAME_MASK(file_name):
        return Store._BOOK_NAME_MASK.match(file_name)

    @staticmethod
    def UNICODE_NAME_MASK(file_name):
        return re.findall(r'(?u)\w+', file_name)

    def _match(self, file_name):
        """
        Regex for file name.

        :param file: filename
        :return: list of result
        """
        if any(file_name.endswith(s) for s in self.SUPPORT_FILE_EXTENSION):
            # cyrillic titles
            return self.UNICODE_NAME_MASK(file_name)

    def _request_data(self, path, b_name, b_type):
        """
        Make data for Executor's execute method (GET to API).

        :param path: absolute path to folder, where is being the book.
        :type path: str
        :param b_name: book name
        :type b_name: str
        :param b_type: one of supported types:
        type b_type: str
        :return: dict
        """
        return OrderedDict(zip(self.REQ_KEYS, (path, b_name, b_type)))

    def get_books(self):
        """
        Get books from store.
        Check supported types of files.
        Make data for Executor's request.

        :return: generator-object of dict
        """
        for path, folders, files in os.walk(self.root_path):
            if path.startswith(st.UNCHECKABLE_FOLDERS):
                continue
            for f in files:
                m = self._match(f)
                if not m:
                    continue
                book_type = m.pop()
                book_name = ' '.join(m)
                yield self._request_data(path, book_name, book_type)

    def init(self):
        """
        Initialize of book store.
        :return:
        """
        return 'init'

    def update(self):
        """
        Update book store.

        :return:
        """
        books = self.get_books()
        self.Executor.execute(books, 'google')

    def remove(self):
        """
        Remove of book store.

        :return:
        """
        return 'remove'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init",
                        help="initialize book store",
                        action="store_true"
                        )
    parser.add_argument("-u", "--update",
                        help="update book store",
                        action="store_true"
                        )
    parser.add_argument("-r", "--remove",
                        help="stop monitoring of book store",
                        action="store_true"
                        )
    args = parser.parse_args()

    store = Store()
    if args.init:
        store.init()
    elif args.update:
        store.update()
    elif args.remove:
        store.remove()
    else:
        store.update()
