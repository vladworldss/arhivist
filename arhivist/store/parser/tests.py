# coding: utf-8
import os
import sys
sys.dont_write_bytecode = True

import pytest
import subprocess as sp
from collections import namedtuple

from . import local


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


@pytest.mark.skip(reason="no way of currently testing this")
def test_get_book_title(test_book='test.pdf', test_path='/tmp'):
    res = call(f'touch {os.path.join(test_path, test_book)}')
    if not res.err:
        res = tuple(x['name'] for x in local.get_book_title('/tmp'))
        assert 'test' in res
        call(f'rm {os.path.join(test_path, test_book)}')
    else:
        raise AssertionError("Test file had't been created!")


@pytest.mark.skip(reason="no way of currently testing this")
def test_all_books(capsys):
    res = len(list(local.get_book_title()))
    with capsys.disabled():
        print(f'\nlen:{res}')


def test_executor_class(capsys):
    from .executor import Executor
    from .api.google import title_task

    def callb(fn):
        with capsys.disabled():
            print(f'\nCallback: {fn.result()}')

    titles = ['Темная башня. Стрелок',
              'Стивен Кинг. Темная башня. Извлечение троих',
              'Стивен Кинг. Темная башня. Бесплодные земли',
              'Стивен Кинг. Темная башня. Колдун и кристалл',
              'Стивен Кинг. Темная башня. Волки Кальи',
              'Стивен Кинг. Темная башня. Песнь Сюзанны',
              'Стивен Кинг. Темная башня. Тёмная Башня',
              'Стивен Кинг. Темная башня. Ветер сквозь замочную скважину'
              ]

    harry = ["Harry Potter and the Philosopher's Stone",
             'Harry Potter and the Chamber of Secrets',
             'Rowling - Harry Potter and the Prisoner of Azkaban',
             'Rowling - Harry Potter and the Goblet of Fire',
             'Rowling - Harry Potter and the Order of the Phoenix',
             'Rowling - Harry Potter and the Half-Blood Prince',
             'Harry Potter and the Deathly Hallows - 2007.epub'
             ]

    ex = Executor(10, title_task, callb, *harry)
    ex.execute()
