# coding: utf-8
import os
import re
from itertools import chain

from .settings import BASE_PATH, SUPPORTED


book_name_mask = re.compile(r'(?P<name>\w+)\.(?P<type>\w+)')
unicode_name_mask = lambda f: re.findall(r'(?u)\w+', f)


def get_book_title(base_path=BASE_PATH):
    """
    Get book title from store folder.

    :param base_path: source path for searching books
    :return: iterator of (path, file_name)
    """

    for path, folders, files in os.walk(base_path):
        for f in files:
            if any(f.endswith(s) for s in SUPPORTED):

                # Для юникодовых названий
                match = unicode_name_mask(f)
                if match:
                    book_name,  book_type = ' '.join(match[:-1]), match[-1]

                    yield ({'path': path, 'name': book_name, 'type': book_type})
                else:
                    print(f)
                    raise NameError('Something wrong')


def load_to_json(titles):
    pass


def load_to_db(titles):
    # Здесь создавать экземпляры моделей и пушить в базу
    pass
