import requests

from arhivist.api.settings import AUTH_URL, CREDENTIALS, BOOKS_URL
from arhivist.api.base import BaseBookApi
from arhivist.parser.item import Book as BookItem


class Book(BaseBookApi):
    """
    Arhivist Books Api.
    See: https://developers.google.com/books/
    """

    BASE_URL = BOOKS_URL

    def __init__(self, *args, **kw):
        self.token = None
        super().__init__(*args, **kw)

    def authorize(self, *args, **kw):
        resp_json = requests.post(url=AUTH_URL, data=CREDENTIALS).json()
        self.token = resp_json["token"]

    def post_book(self, book):
        if not isinstance(book, BookItem):
            raise TypeError
        json_data = {"books": [book.to_dict()]}
        resp = requests.post(url=BOOKS_URL,
                             json=json_data,
                             headers={'Authorization': f'JWT {self.token}'}
                             )
        assert resp.status_code == requests.status_codes.codes.created
        return resp
