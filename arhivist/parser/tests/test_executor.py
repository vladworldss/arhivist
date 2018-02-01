from arhivist.parser.item import Book
from arhivist.parser.executor.book import BookExecutorFactory


def test_book_executor_factory():
    kw = ["/home/books/Harry Potter and the Philosopher's Stone.pdf",
        "Harry Potter and the Philosopher's Stone",
          "pdf"
          ]
    book = Book(*kw)
    ex = BookExecutorFactory.make_init_executor("google")
    res = ex.execute([book], callback=False)
    assert res