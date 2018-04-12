# coding: utf-8
# flake8: noqa
"""
Модуль логирования.
"""
import os
import logging
import time
from hashlib import md5

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2018, Vladimir Gerasimenko"
__version__    = "1.0.2"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


def get_current_time():
    """
    Возращает текущее время в формате "%Y.%m.%d_%H:%M:%S".
    :return: str
    """
    return time.strftime("%Y.%m.%d_%H:%M:%S")


def get_unique_name(name, hex_id=False):
    """
    К переданному имени добавляется уникальный id,
    вычисленный на основе текущей даты+времени.

    :param name: базовое имя, к которому будет добавляться уникальный id
    :param hex_id: если True - id будет hex_hash от текущего времени
    :return: str name_id
    """
    unique_id = get_current_time()

    if hex_id:
        hash_time = md5(unique_id.encode("utf-8"))
        unique_id = hash_time.hexdigest()
    unique_name = f"{name}_{unique_id}"
    return unique_name


class Logger(object):
    """
    Обертка над Logging.
    """
    __LogCls = logging
    __LOG_FILE_EXT = "log"

    def __init__(self, log_dir, log_file_name):

        self.__log_dir = log_dir
        self.__log_file_name = log_file_name
        self.__log_file = None
        self.__logger = None

        self.__set_logger()

    def __set_logger(self):
        unique_name = get_unique_name(self.__log_file_name, hex_id=True)
        logger = self.__LogCls.getLogger(unique_name)
        logger.setLevel(self.__LogCls.INFO)

        # create the logging file handler
        fh = self.__LogCls.FileHandler(self.log_file)
        formatter = self.__LogCls.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        # add handler to logger object
        logger.addHandler(fh)
        self.__logger = logger

    @property
    def log_file(self):
        if self.__log_file is None:
            log_file_name = ".".join([self.__log_file_name, self.__LOG_FILE_EXT])
            self.__log_file = os.path.join(self.__log_dir, log_file_name)
        return self.__log_file

    def info(self, *args, **kw):
        return self.__logger.info(*args, **kw)
