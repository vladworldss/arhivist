
import os
from .conftest import *
from arhivist.parser.executor import BookExecutor


def test_thumbnail_dir(GoogleApi, capsys):
    with capsys.disabled():
        print(GoogleApi.download_dir)
    assert GoogleApi.download_dir == '/home/vladworldss/PycharmProjects/arhivist/arhivist/books/static/thumbnail'


def test_execute_without_callback(books, GoogleApi, capsys):
    BookExecutor.execute(books, 'google', callback=False)
    pngs = set((x for x in os.listdir(GoogleApi.download_dir) if x.endswith('.png')))
    pngs.remove('test_thumb.png')
    assert pngs

