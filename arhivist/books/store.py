# coding: utf-8
import os

from .settings import *
from parser.executor import Executor


def get_books(root_path=STORE_PATH):
    for path, folders, files in os.walk(root_path):
        for f in files:
            if any(f.endswith(s) for s in SUPPORT_TYPES):
                # For Cyrillic titles
                match = UNICODE_NAME_MASK(f)
                if match:
                    book_name, book_type = ' '.join(match[:-1]), match[-1]
                    yield {'path': path, 'raw_title': book_name, 'type': book_type}
                else:
                    raise NameError('Something wrong')

def update():
    books = get_books()
    bad = []
    # TODO: можно сделать подобие reduce bad передавать в след api
    for res in Executor.execute('Books', books, 'google', POST_URL):
        if res.get('status') == 'BAD':
            bad.append(res)


def init():
    pass

def remove():
    pass