# coding: utf-8
"""
Interface for Arhivist Async API.
"""
from aiohttp import request

from arhivist.api.settings import AUTH_URL, CREDENTIALS, BOOKS_URL
from arhivist.api.base import BaseBookApi
from arhivist.parser.item import Book as BookItem


class Book(BaseBookApi):

    BASE_URL = BOOKS_URL

    def __init__(self, *args, **kw):
        self.__token = None
        super().__init__(*args, **kw)

    @property
    def token_header(self):
        return {'Authorization': f'JWT {self.__token}'}

    async def authorize(self, *args, **kw):
        try:
            resp = await request("POST", AUTH_URL, data=CREDENTIALS)
        except Exception as e:
            return self.make_bad_responce(401, e)
        resp_json = await resp.json()
        self.__token = resp_json["token"]

    async def post_book(self, book):
        if not isinstance(book, BookItem):
            raise TypeError
        json_data = {"books": [book.to_dict()]}
        try:
            resp = await request("POST",
                                 BOOKS_URL,
                                 json=json_data,
                                 headers=self.token_header
                                 )
        except Exception as e:
            return self.make_bad_responce(500, e)
        return resp
