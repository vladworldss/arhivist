import pytest
import requests

from arhivist.parser.item import Book
from arhivist.parser.executor.book import BookExecutorFactory

@pytest.mark.skip(reason="no way of currently testing this")
def test_book_executor_factory():
    kw = ["/home/books/Harry Potter and the Philosopher's Stone.pdf",
        "Harry Potter and the Philosopher's Stone",
          "pdf"
          ]

    books = [Book(*kw) for _ in range(10)]
    ex = BookExecutorFactory.make_init_executor("google")
    res = ex.execute(books, max_workers=100, callback=False)
    assert res

@pytest.mark.skip(reason="no way of currently testing this")
def test_search_unicode_book():
    kw = ["Гарри Поттер и Узник Азкабана.djv",
        "Гарри Поттер и Узник Азкабана",
          "djv"
          ]

    books = [Book(*kw)]
    ex = BookExecutorFactory.make_init_executor("google")
    res = ex.execute(books, max_workers=1, callback=False)
    assert [x.to_json() for x in res]


def test_init():
    kw = ["/home/books/Harry Potter and the Philosopher's Stone.pdf",
        "Harry Potter and the Philosopher's Stone",
          "pdf"
          ]

    books = [Book(*kw) for _ in range(1)]
    ex = BookExecutorFactory.make_init_executor("google")
    res = ex.execute(books, max_workers=1, callback=True)
    assert res
