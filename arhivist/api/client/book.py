# coding: utf-8
"""
Interface for Arhivist API.
"""
import requests

from arhivist.api.settings import AUTH_URL, CREDENTIALS, BOOKS_URL, BOOK_URL
from arhivist.api.base import BaseBookApi
from arhivist.parser.item import Book as BookItem


class Book(BaseBookApi):
    """
    Arhivist Books Api.
    See: localhost/api
    """

    BASE_URL = BOOKS_URL

    def __init__(self, *args, **kw):
        self.__token = None
        super().__init__(*args, **kw)

    @property
    def token_header(self):
        return {'Authorization': f'JWT {self.__token}'}

    def authorize(self, *args, **kw):
        resp_json = requests.post(url=AUTH_URL, data=CREDENTIALS).json()
        self.__token = resp_json["token"]

    def post_book(self, book):
        if not isinstance(book, BookItem):
            raise TypeError
        json_data = {"books": [book.to_dict()]}
        return requests.post(url=BOOKS_URL,
                             json=json_data,
                             headers=self.token_header
                             )

    def get_book(self, book_id):
        if not isinstance(book_id, int):
            raise TypeError
        book_url = f"{BOOKS_URL}{book_id}"
        return requests.get(url=book_url,
                            headers=self.token_header
                            )

    def get_all_books(self):
        return requests.get(url=BOOKS_URL,
                            headers=self.token_header
                            )

    def delete_book(self, book_id):
        book_url = f"{BOOK_URL}{book_id}"
        return requests.delete(url=book_url,
                               headers=self.token_header
                             )

    def search_book(self, title):
        """
        Searching book from book_title.
        If book had found, return json.

        :return:
        """

        search_url = BOOKS_URL + "search/" + title
        book_resp = requests.get(url=search_url,
                                 headers=self.token_header
                                 )
        if book_resp.status_code in {self.status_codes.created, self.status_codes.ok}:
            return book_resp.json()
