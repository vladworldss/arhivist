# coding: utf-8
import os

from .settings import BASE_PATH, SUPPORT_TYPES, UNICODE_NAME_MASK

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


def book_raw_data(base_path=BASE_PATH):
    """
    Iterator who's returned raw data for books from store folder.

    :param base_path: source path for searching books
    :yield: dict(path, name, type)
    """

    for path, folders, files in os.walk(base_path):
        for f in files:
            if any(f.endswith(s) for s in SUPPORT_TYPES):

                # For unicode titles (cyrillic)
                match = UNICODE_NAME_MASK(f)
                if match:
                    book_name,  book_type = ' '.join(match[:-1]), match[-1]
                    yield {'path': path, 'name': book_name, 'type': book_type}
                else:
                    raise NameError('Something wrong')


def load_to_json(titles, out_file='books'):
    pass


def load_to_db(titles):
    # Здесь создавать экземпляры моделей и пушить в базу
    pass
