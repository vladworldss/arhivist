# coding: utf-8
"""
Module of Sxecutor's tests.
"""

import pytest
import os

from arhivist.parser.item import Book
from arhivist.parser.executor.book import BookExecutorFactory

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2018, Vladimir Gerasimenko"
__version__    = "0.0.2"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


def make_test_books(title, folder):
    book_path = os.path.join(folder, title)
    with open(book_path, "w") as out:
        out.write("START")
    assert os.path.exists(book_path)
    return book_path


@pytest.mark.skip(reason="no way of currently testing this")
def test_get_books(store, book_files):
    root_path = "/home/test/books"

    ex_books = set()
    for file in book_files:
        book_path = make_test_books(file, root_path)
        ex_books.add(Book(book_path, *Book.match(file)))

    store.root_path = root_path
    store_books = set([x for x in store.get_all_books()])

    ex_books_titles = set((x.raw_title for x in ex_books))
    store_books_titles = set((x.raw_title for x in store_books))
    assert ex_books_titles.issubset(store_books_titles)
    assert all(isinstance(x, Book) for x in store_books)


def test_init(store, book_files):
    root_path = "/home/test/books"

    ex_books = set()
    for file in book_files:
        book_path = make_test_books(file, root_path)
        ex_books.add(Book(book_path, *Book.match(file)))

    store.root_path = root_path
    store.init(vendor="google")


def test_update():
    pass


def test_delete():
    pass
