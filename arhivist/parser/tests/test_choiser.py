# coding: utf-8
"""
Module of Choiser's tests.
"""
import pytest

from arhivist.api.choiser import Choiser
from arhivist.parser.item import Book
from arhivist.parser.executor.book import BookExecutorFactory

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2018, Vladimir Gerasimenko"
__version__    = "0.0.2"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


resps = [
    {"title": "J.K.Roling. Harry Potter and the Philosopher's Stone some_text"},
    {"title": "J.K.Roling. Harry Potter and the Philosopher's Stone"},  # best
    {"title": "01 Harry Potter and the Goblet of Fire"},
    {"title": "Full Complete story: Harry Potter"},
]

@pytest.mark.skip(reason="no way of currently testing this")
def test_best_choise():
    title = "01 J K Roling. Harry Potter and the Philosopher's Stone"
    best = Choiser.best_choise(value=title, choises=resps, field="title")
    assert best == resps[1]

@pytest.mark.skip(reason="no way of currently testing this")
def test_best_book_choise():
    title = "01 J K Roling. Harry Potter and the Philosopher's Stone"
    best = Choiser.best_book_choise(value=title, choises=resps)
    assert best == resps[1]

def test_empty_choise(bad_title_book_kwarg):
    books = [Book(**bad_title_book_kwarg)]
    ex = BookExecutorFactory.make_init_executor("google")
    res = ex.execute(books, max_workers=1, callback=False)
    assert res
