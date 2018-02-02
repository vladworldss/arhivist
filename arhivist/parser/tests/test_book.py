# coding: utf-8
"""
Module of Book's tests.
"""
import pytest
import json

from arhivist.parser.item import Book

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2018, Vladimir Gerasimenko"
__version__    = "0.0.2"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


@pytest.mark.parametrize(
    "title,result", [
        ("Harry Potter and the Philosopher's Stone.pdf", ("Harry Potter and the Philosopher's Stone", "pdf")),
        ("Harry Potter and the Chamber of Secrets.djvu", ("Harry Potter and the Chamber of Secrets", "djvu")),
        ("Гарри Поттер и Узник Азкабана.djv", ("Гарри Поттер и Узник Азкабана", "djv")),
        ("01 Harry Potter and the Goblet of Fire.epub", ("01 Harry Potter and the Goblet of Fire", "epub")),
        ("Harry_Potter_and_the_Order of the Phoenix.fb2", ("Harry_Potter_and_the_Order of the Phoenix", "fb2")),
        ("Harry Potter and the Half-Blood Prince.avi", None),
        ("__Harry Potter and the Deathly Hallows.mp3", None)
    ]
)
def test_match_title(title, result):
    m = Book.match(title)
    assert  m == result

def test_to_json(harry_book_args):
    b = Book(*harry_book_args)
    json_book = b.to_json()
    assert all([x in json_book for x in harry_book_args])

def test_from_json(harry_book_kwargs):
    js = json.dumps(harry_book_kwargs)
    b = Book.from_json(js)
    assert all(getattr(b, key) == value for key, value in harry_book_kwargs.items())

@pytest.mark.skip(reason="does not implement")
def test_get_meta():
    pass

def test_update(harry_book_args):
    b = Book(*harry_book_args)
    json_str = '{"publisher": "OREALLY", "category": "FICTION"}'
    with pytest.raises(TypeError):
        b.update(json_str)
    dict_field = json.loads(json_str)
    b.update(dict_field)
    assert b.publisher == "OREALLY"
    assert b.category == "FICTION"

def test_encode(harry_book_args):
    class MyEncoder(json.JSONEncoder):
        def default(self, o):
            return o.to_dict()

    b = Book(*harry_book_args)
    assert json.dumps(MyEncoder().encode(b))
    assert json.dumps(b.to_dict())
