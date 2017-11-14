# coding: utf-8
"""
Pytest fixtures.
"""
import pytest

from arhivist.parser.settings import THUMBNAIL_DIR
from arhivist.parser.api.google import Book as GoogleBook
from arhivist.parser.store import Store

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "gerasimenko.vladimir@globinform.ru"


@pytest.yield_fixture(scope='module')
def books():
    test_folder = '/tmp/Arhivist'
    store = Store(test_folder)
    yield store.get_books()

@pytest.yield_fixture(scope='module')
def GoogleApi():
    yield GoogleBook(download_dir=THUMBNAIL_DIR)
