import sys
sys.dont_write_bytecode = True
import pytest

from arhivist.parser import Store


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
