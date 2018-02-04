# coding: utf-8
"""
Module of BookExecutor classes.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .base import ExecutorFactory, init_api, PoolExecutor
from arhivist.parser.settings import THUMBNAIL_DIR

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"

# TODO: включить в конструктор store или manage.py
if not os.path.exists(os.path.exists(THUMBNAIL_DIR)):
    os.makedirs(THUMBNAIL_DIR, exist_ok=True)

class BookExecutorFactory(ExecutorFactory):

    ItemType = "Book"

    # ---------
    @classmethod
    @init_api
    def make_init_executor(cls, vendor, *args, **kw):
        return cls.__InitExecutor(task_api=kw["vendor_api"], callback_api=kw["arhivist_api"])

    @classmethod
    @init_api
    def make_update_executor(cls, vendor, *args, **kw):
        return cls.__UpdateExecutor(task_api=kw["arhivist_api"], callback_api=kw["vendor_api"])

    @classmethod
    @init_api
    def make_delete_executor(cls, vendor, *args, **kw):
        return cls.__DeleteExecutor(task_api=kw["arhivist_api"])

    # ---------
    class __InitExecutor(PoolExecutor):

        def task(self, book):
            b_resp = self.task_api.search_book(title=book.raw_title)
            if not b_resp:
                book._bad = self.task_api.make_bad_responce(204, "No Content")
            else:
                book.update(b_resp)
                book.thumbnail.name = self.task_api.download_thumbnail(
                    url=book.thumbnail.volume_link, download_dir=THUMBNAIL_DIR
                )
            return book

        def callback(self, fn):
            if fn.cancelled():
                fn.arg._bad = self.callback_api.make_bad_responce(205, "Reset Content. Cancelled")
            elif fn.done():
                error = fn.exception()
                if not error:
                    book = fn.result()
                    if book._bad:
                        return
                    resp = self.callback_api.post_book(book)
                    if resp.status_code != self.callback_api.status_codes.created:
                        book._bad = self.callback_api.make_bad_responce(
                            resp.status_code,
                            resp.content.decode("utf-8")
                        )

    # ---------
    class __UpdateExecutor(PoolExecutor):

        def task(self):
            pass

        def callback(self):
            pass

    # ---------
    class __DeleteExecutor(PoolExecutor):

        def task(self):
            pass
