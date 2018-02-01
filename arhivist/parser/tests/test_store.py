import pytest
import os

from arhivist.parser.item import Book


def test_get_books(store, book_files):
    root_path = "/home/test/books"

    ex_books = set()
    for file in book_files:
        book_path = os.path.join(root_path, file)
        with open(book_path, "w") as out:
            out.write("START")
        assert os.path.exists(book_path)
        ex_books.add(Book(book_path, *Book.match(file)))

    store.root_path = root_path
    store_books = set([x for x in store.get_all_books()])

    ex_books_titles = set((x.raw_title for x in ex_books))
    store_books_titles = set((x.raw_title for x in store_books))
    assert ex_books_titles.issubset(store_books_titles)
    assert all(isinstance(x, Book) for x in store_books)


def test_init():
    pass

def test_update():
    pass


def test_delete():
    pass
