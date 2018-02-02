# coding: utf-8
"""
Module of Pytest Arhivist fixtures.
"""
import sys
sys.dont_write_bytecode = True
import pytest

from arhivist.parser import Store

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2018, Vladimir Gerasimenko"
__version__    = "0.0.2"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


@pytest.yield_fixture(scope='module')
def store():
    yield Store()

@pytest.yield_fixture(scope='module')
def book_files():
    yield ["Harry Potter and the Philosopher's Stone.pdf",
           "Harry Potter and the Chamber of Secrets.djvu",
           "Гарри Поттер и Узник Азкабана.djv",
           "01 Harry Potter and the Goblet of Fire.epub",
           "Harry_Potter_and_the_Order of the Phoenix.fb2"
           ]

@pytest.yield_fixture(scope='module')
def harry_book_args():
    yield [
        "/home/books/Harry Potter and the Philosopher's Stone.pdf",
        "Harry Potter and the Philosopher's Stone",
        "pdf"
    ]

@pytest.yield_fixture(scope='module')
def harry_book_kwargs():
    yield {
        "raw_title": "Harry Potter and the Philosopher's Stone",
        "path": "/home/books/Harry Potter and the Philosopher's Stone.pdf",
        "file_ext": "pdf"
    }

@pytest.yield_fixture(scope='module')
def harry_unicode_book_args():
    yield [
        "/home/books/Гарри Поттер и Узник Азкабана.djv",
        "Гарри Поттер и Узник Азкабана",
        "djv"
    ]
