# coding: utf-8
"""
Pytest fixtures.
"""
import sys
sys.dont_write_bytecode = True
import pytest

from arhivist.api.client import Book as ArhivistBookClient
from arhivist.parser.tests.conftest import harry_unicode_book_args

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "gerasimenko.vladimir@globinform.ru"


@pytest.yield_fixture(scope='module')
def ArhClient():
    c = ArhivistBookClient()
    yield c
