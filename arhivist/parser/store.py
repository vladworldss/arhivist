# coding: utf-8
"""
Module for working with book store.
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import argparse

from arhivist.parser.executor import BookExecutorFactory
from arhivist.parser.item import Book
from arhivist.parser import settings as st
from arhivist.parser.logger import Logger

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class Store(object):
    """
    Book store class.
    """
    __LoggerCls = Logger

    def __init__(self, root_path=st.STORE_PATH, ExecutorFactory=BookExecutorFactory, BookCls=Book):
        self.root_path = root_path
        self.ExecutorFactory = ExecutorFactory
        self.BookCls = BookCls

        self.__set_logger()

        self.logger.info("*" * 50)
        self.logger.info("Init store.")
        self.logger.info(f"Store dir: {root_path}")
        self.logger.info(f"Thumbnail dir: {st.THUMBNAIL_DIR}")

    def __del__(self):
        self.logger.info("*" * 50)

    def __set_logger(self, log_file_name="parser"):
        logger_dir = os.path.dirname(__file__)
        self.__logger = self.__LoggerCls(logger_dir, log_file_name)

    @property
    def logger(self):
        return self.__logger

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
        vendor = kw["vendor"]
        self.logger.info("-" * 50)
        self.logger.info(f"Init of store for vendor={vendor} has started.")
        books = self.get_all_books()
        ex = self.ExecutorFactory.make_init_executor(vendor)
        res = ex.execute(books, callback=True)

        # Unknown books
        self.logger.info("-"*50)
        self.logger.info("[Unknown books:]")
        for b in res["bad"]:
            self.logger.info(f"{b.raw_title}, {b._bad}")

        # Known books
        self.logger.info("-" * 50)
        self.logger.info("[Known books:]")
        for b in res["ok"]:
            self.logger.info(f"{b.raw_title}")
        self.logger.info("-" * 50)


    def update(self, **kw):
        """
        Update book store.

        :return:
        """
        vendor = kw["vendor"]
        self.logger.info("-" * 50)
        self.logger.info(f"Updating of store for vendor={vendor} has started.")
        books = self.get_all_books()
        ex = self.ExecutorFactory.make_update_executor(vendor)
        res = ex.execute(books, callback=True)

        # Unknown books
        self.logger.info("-" * 50)
        self.logger.info("[Unknown books:]")
        for b in res["bad"]:
            self.logger.info(f"{b.raw_title}, {b._bad}")

        # Known books
        self.logger.info("-" * 50)
        self.logger.info("[Known books:]")
        for b in res["ok"]:
            self.logger.info(f"{b.raw_title}")
        self.logger.info("-" * 50)


    def delete(self, **kw):
        """
        Remove of all books store.

        :return:
        """
        vendor = kw["vendor"]
        self.logger.info("-" * 50)
        self.logger.info(f"Deleting of store for vendor={vendor} has started.")
        books = self.get_all_books()
        ex = self.ExecutorFactory.make_delete_executor(vendor)
        res = ex.execute(books)

        # Undeleted books
        self.logger.info("-" * 50)
        self.logger.info("[Undeleted books:]")
        for b in res["bad"]:
            self.logger.info(f"{b.raw_title}, {b._bad}")

        # Deleted books
        self.logger.info("-" * 50)
        self.logger.info("[Deleted books:]")
        for b in res["ok"]:
            self.logger.info(f"{b.raw_title}")

    @classmethod
    def execute(cls):
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
                            default=st.VENDORS[0],
                            choices=st.VENDORS,
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


def execute_from_command_line(argv=None):
    """Run a ManagementUtility."""

    Store.execute()


if __name__ == "__main__":
    execute_from_command_line()