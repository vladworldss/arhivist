# coding: utf-8
from collections import namedtuple
import os
import pytest
from pprint import pprint
import sys
import subprocess as sp

from .api.google import title_task
from .executor import Executor
from . local import book_raw_data

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"

sys.dont_write_bytecode = True


def call(cmd):
    """
    Запускает переданную комманду в терминале, предварительно получив stdout, stderr.

    :param cmd:
    :return:
    """
    result = namedtuple('result', ['err', 'out'])
    with sp.Popen(cmd, shell=True, executable='/bin/bash', stdout=sp.PIPE, stderr=sp.PIPE) as pipe:
        err = pipe.stderr.readlines()
        out = pipe.stdout.readlines()
    result.err, result.out = err, out
    return result


@pytest.yield_fixture
def tmp_book():
    base_name = 'test'
    book_type = '.pdf'
    path = '/tmp'
    abs_name = os.path.join(path, base_name+book_type)

    call(f'touch {abs_name}')
    yield base_name, path
    call(f'rm {abs_name}')


def test_get_book_title(tmp_book):
    name, path = tmp_book
    res = tuple(x['name'] for x in book_raw_data(path))
    assert name in res


def test_empty_folder(capsys):
    res = len(list(book_raw_data()))
    assert res != 0


#@pytest.mark.skip(reason='No')
def test_executor_class(capsys):

    def callb(fn):
        with capsys.disabled():
            if fn.done:
                print(f'\nCallback: {fn.result()}')

    titles = ['Темная башня. Стрелок',
              'Стивен Кинг. Темная башня. Извлечение троих',
              'Стивен Кинг. Темная башня. Бесплодные земли',
              'Стивен Кинг. Темная башня. Колдун и кристалл',
              'Стивен Кинг. Темная башня. Волки Кальи',
              'Стивен Кинг. Темная башня. Песнь Сюзанны',
              'Стивен Кинг. Темная башня. Тёмная Башня',
              'Стивен Кинг. Темная башня. Ветер сквозь замочную скважину',
              "Harry Potter and the Philosopher's Stone",
              'Harry Potter and the Chamber of Secrets',
              'Harry Potter and the Prisoner of Azkaban',
              'Harry Potter and the Goblet of Fire',
              'Harry Potter and the Order of the Phoenix',
              'Harry Potter and the Half-Blood Prince',
              'Harry Potter and the Deathly Hallows'
              ]

    ex = Executor(30, title_task, callb, *titles)
    ex.execute()
