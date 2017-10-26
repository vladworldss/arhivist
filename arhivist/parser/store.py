# coding: utf-8
import os
import re
import argparse

from executor import BookExecutor
from settings import STORE_PATH, UNCHECKABLE_FOLDERS


class Store(object):

    SUPPORT_TYPES = {'pdf', 'djvu', 'djv', 'epub', 'fb2'}
    BOOK_NAME_MASK = re.compile(r'(?P<name>\w+)\.(?P<type>\w+)')
    UNICODE_NAME_MASK = lambda self, f: re.findall(r'(?u)\w+', f)

    def __init__(self, root_path=STORE_PATH):
        self.root_path = root_path
        self.Executor = BookExecutor

    def _match(self, file):
        if any(file.endswith(s) for s in self.SUPPORT_TYPES):
            # cyrillic titles
            return self.UNICODE_NAME_MASK(file)

    def _get_books(self):
        for path, folders, files in os.walk(self.root_path):
            if path.startswith(UNCHECKABLE_FOLDERS):
                continue
            for f in files:
                m = self._match(f)
                if not m:
                    continue
                book_name = m.pop()
                book_type = ' '.join(m)
                yield {'path': path,
                       'raw_title': book_name,
                       'type': book_type,
                       'result': None
                       }

    def init(self):
        pass

    def update(self):
        books = self._get_books()
        self.Executor.execute(books, 'google')

    def remove(self):
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init",
                        help="initialize book store",
                        action="store_true"
                        )
    parser.add_argument("-u", "--update",
                        help="update book store",
                        action="store_true"
                        )
    parser.add_argument("-r", "--remove",
                        help="stop monitoring of book store",
                        action="store_true"
                        )
    args = parser.parse_args()

    store = Store()
    if args.init:
        store.init()
    elif args.update:
        store.update()
    elif args.remove:
        store.remove()
    else:
        store.update()
