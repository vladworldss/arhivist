# coding: utf-8
from concurrent.futures import ThreadPoolExecutor, as_completed, wait

from .local import get_book_title
from .api.google import Api
from time import time


class Executor(ThreadPoolExecutor):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.__task = None
        self.__args = []
        self.__callback = None
        self.__futures = []

        # set task
        task = kw.get('task')
        if callable(task):
            self.__task = task
        else:
            raise TypeError('Task object must be callable')

        # set args for task
        _args = kw.get('args')
        if hasattr(_args, '__iter__'):
            self.__args = _args
        elif _args:
            self.__args.append(_args)

        # make futures
        self.__futures = tuple(map(lambda x: self.submit(*x), ((self.__task, x) for x in self.__args)))

        # set callback
        _cbk = kw.get('callback')
        if callable(_cbk):
            for f in self.__futures:
                f.add_done_callback(_cbk)

    def execute(self):
        if not self.__task:
            raise Exception("Tasks does't exist")

        waitable = as_completed
        if not self.__callback:
            waitable = wait
        return tuple(map(lambda x: x.result(), waitable(self.__futures)))



def task(title):
    req = f'intitle:{title}'
    volumes = Api()
    return volumes.list(req)

def foo():
    # titles = tuple((x['name'] for x in get_book_title()))[:30]
    titles = ['Темная башня. Стрелок',
              # 'Стивен Кинг. Темная башня. Извлечение троих',
              # 'Стивен Кинг. Темная башня. Бесплодные земли',
              # 'Стивен Кинг. Темная башня. Колдун и кристалл',
              # 'Стивен Кинг. Темная башня. Волки Кальи',
              # 'Стивен Кинг. Темная башня. Песнь Сюзанны',
              # 'Стивен Кинг. Темная башня. Тёмная Башня',
              # 'Стивен Кинг. Темная башня. Ветер сквозь замочную скважину'
              ]

    ex = ThreadPoolExecutor(max_workers=30)
    futures = [ex.submit(task, t) for t in titles]
    results = []

    for f in as_completed(futures):
        results.append(f.result())
    return results
