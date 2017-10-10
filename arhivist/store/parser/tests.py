# coding: utf-8
import os
import sys
sys.dont_write_bytecode = True

import subprocess as sp
import pytest
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


def test_get_book_title(test_book='test.pdf', test_path='/tmp'):
    res = call(f'touch {os.path.join(test_path, test_book)}')
    if not res.err:
        res = tuple(x['name'] for x in local.get_book_title('/tmp'))
        assert 'test' in res
        call(f'rm {os.path.join(test_path, test_book)}')
    else:
        raise AssertionError("Test file had't been created!")


def test_all_books(capsys):
    res = len(list(local.get_book_title()))
    with capsys.disabled():
        print(f'\nlen:{res}')
