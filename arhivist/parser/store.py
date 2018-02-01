# coding: utf-8
"""
Module for working with book store.
"""
import os
import sys
sys.path.append(__file__)
import argparse

from arhivist.parser.executor import BookExecutorFactory
from arhivist.parser.item import Book
from arhivist.parser import settings as st

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class Store(object):
    """
    Book store class.
    """

    def __init__(self, root_path=st.STORE_PATH, ExecutorFactory=BookExecutorFactory, BookCls=Book):
        self.root_path = root_path
        self.ExecutorFactory = ExecutorFactory
        self.BookCls = BookCls

    def make_thumbnail_folder(self):
        if not os.path.exists(st.THUMBNAIL_DIR):
            os.makedirs(st.THUMBNAIL_DIR, exist_ok=True)

    def get_all_books(self):
        """
        Get books from store.
        Check supported types of files.
        Make data for Executor's request.

        :return: self.Book
        """
        for path, folders, files in os.walk(self.root_path):
            if path.startswith(st.UNCHECKABLE_FOLDERS):
                continue
            for f in files:
                m = self.BookCls.match(f)
                if m:
                    yield self.BookCls(path, *m)

    def init(self, **kw):
        """
        Initialize of book store.
        :return:
        """
        books = self.get_all_books()
        ex = self.ExecutorFactory.make_init_executor(kw["vendor"])
        res = ex.execute(books, callback=False)

    def update(self, **kw):
        """
        Update book store.

        :return:
        """
        books = self.get_all_books()
        ex = self.ExecutorFactory.make_update_executor(kw["vendor"])
        ex.execute(books)

    def delete(self, **kw):
        """
        Remove of book store.

        :return:
        """
        books = self.get_all_books()
        ex = self.ExecutorFactory.make_delete_executor(kw["vendor"])
        ex.execute(books)


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

    parser.add_argument("-vnd", "--vendor",
                        type=str,
                        default=st.vendors[0],
                        choices=st.vendors,
                        help="search book with vendor-api",
                        )

    args = parser.parse_args()
    store = Store()

    if args.init:
        store.init(vendor=args.vendor)
    elif args.update:
        store.update(vendor=args.vendor)
    elif args.remove:
        store.delete(vendor=args.vendor)
    else:
        store.init()
