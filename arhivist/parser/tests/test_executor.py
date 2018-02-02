# coding: utf-8
"""
Module of Executor's tests.
"""
import pytest

from arhivist.parser.item import Book
from arhivist.parser.executor.book import BookExecutorFactory

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2018, Vladimir Gerasimenko"
__version__    = "0.0.2"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"

# @pytest.mark.skip(reason="no way of currently testing this")
def test_book_executor_factory(harry_book_args):
    books = [Book(*harry_book_args) for _ in range(10)]
    ex = BookExecutorFactory.make_init_executor("google")
    res = ex.execute(books, max_workers=10, callback=False)
    assert res

# @pytest.mark.skip(reason="no way of currently testing this")
def test_search_unicode_book(harry_unicode_book_args):
    books = [Book(*harry_unicode_book_args)]
    ex = BookExecutorFactory.make_init_executor("google")
    res = ex.execute(books, max_workers=1, callback=False)
    assert [x.to_json() for x in res]
