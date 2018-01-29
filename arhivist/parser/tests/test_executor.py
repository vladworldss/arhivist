from arhivist.parser.book import Book
from arhivist.parser.executor.book import BookExecutorFactory


def test_book_executor_factory():
    kw = ["Harry Potter and the Philosopher's Stone",
          "/home/books/Harry Potter and the Philosopher's Stone.pdf",
          "pdf"
          ]
    book = Book(*kw)
    ex = BookExecutorFactory.make_init_executor("google")
    ex.execute([book], callback=False)
