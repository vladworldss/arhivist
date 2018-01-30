import pytest

from arhivist.parser.models import Book


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


def test_book_json():
    kw = ["Harry Potter and the Philosopher's Stone",
          "/home/books/Harry Potter and the Philosopher's Stone.pdf",
          "pdf"
          ]
    b = Book(*kw)
    json_book = b.to_json()
    assert all([x in json_book for x in kw ])
