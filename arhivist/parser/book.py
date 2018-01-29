# coding: utf-8
"""
Module of the Book class.
"""
import re
import json
import requests

from .settings import SUPPORT_BOOK_EXTENSION
__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"
__all__        = ("BooksList", "BookDetail", "CategoryList")


class Book(object):

    __BOOK_NAME_MASK = re.compile(r'(?P<name>\w+)\.(?P<type>\w+)')

    __SUPPORTED = SUPPORT_BOOK_EXTENSION

    __slots__ = ("publisher", "description", "language", "published_date",
                 "title", "page_count", "volume_link", "isbn_10",
                 "isbn_13", "author", "category", "thumbnail", "path", "raw_title",
                 "file_ext"
                 )

    def __init__(self, raw_title, path, file_ext):
        for attr in self.__slots__:
            setattr(self, attr, None)

        self.raw_title = raw_title
        self.path = path
        self.file_ext = file_ext
        self.thumbnail = Thumbnail()

    @staticmethod
    def from_json(_json):
        raise NotImplementedError

    def to_json(self):
        """
        Convert self-instance to json-str.

        :return:
        """
        return json.dumps({x: getattr(self, x) for x in self.__slots__})

    def update(self, _json):
        """
        Update book fields from json

        :param resp_json:
        :return:
        """
        raise NotImplementedError

    def get_meta(self):
        """
        Get meta-info of the book from embedded descr.

        :return:
        """
        raise NotImplementedError

    @classmethod
    def __book_name_match(cls, file_name):
        """
        Regex for book-title.

        :param str file_name:
        :return:
        """
        return cls.__BOOK_NAME_MASK.match(file_name)

    @staticmethod
    def __unicode_name_match(file_name):
        """
        Regex for unicode-book-title.

        :param str file_name:
        :return:
        """
        return re.findall(r'(?u)[\w\']+', file_name)

    @classmethod
    def match(cls, file_name):
        """
        Determines whether the file is a book. If it's true, return list of attrs

        :param str file_name: filename
        :return: ("title", "file_ext") or None
        """
        if any(file_name.endswith(s) for s in cls.__SUPPORTED):

            # match cyrillic titles
            m = cls.__unicode_name_match(file_name)
            if m:
                book_type = m.pop()
                book_name = " ".join(m)
                return (book_name, book_type)


class Thumbnail(object):

    __slots__ = ("id", "volume_link")

    def __init__(self, _id=None, volume_link=None):
        self.id = _id
        self.volume_link = volume_link

    @staticmethod
    def get_thumbnail(url, w='w300'):
        """
        Save thumbnail from responce.

        :param url: thumbnail url
        like 'http://books.google.com/books/content?
                    id=junUDQAAQBAJ&
                    printsec=frontcover&
                    img=1&
                    zoom=1&
                    edge=curl&
                    source=gbs_api'

        :param w: weight
        :return:
        """
        url = '{}&fife={}'.format(url, w)
        return requests.get(url, stream=True)

    def get_id_thumbnail(self, url):
        match = self.ID_THUMBNAIL.match(url)
        if not match:
            raise Exception
        return match.groupdict()['id']

    @staticmethod
    def save_thumbnail(resp, path):
        """
        Save thumbnail.

        :param resp: responce from request
        :param path: path to save image
        :return:
        """
        with open(path, 'wb') as f:
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, f)

    def download_thumbnail(self, resp):
        t_url = resp['thumbnail']['url']
        t_id = self.get_id_thumbnail(t_url)

        t_resp = self.get_thumbnail(t_url)
        t_name = f"{t_id}.png"
        full_path = os.path.join(self.download_dir, t_name)
        self.save_thumbnail(t_resp, full_path)
        resp['thumbnail'] = t_name
