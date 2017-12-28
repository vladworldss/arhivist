# coding: utf-8
import abc


class AbsBook(metaclass=abc.ABCMeta):
    """
    Abstract base class for search book with api
    """

    @abc.abstractmethod
    def get(self, volumeId, **kwargs):
        """
        Retrieves a Volume resource based on ID
        volumeId -- ID of volume to retrieve.

        :param volumeId:
        :param kwargs:
        :return: responce (json)
        """
        pass

    @abc.abstractmethod
    def list(self, q, **kwargs):
        """
        Performs a book search.
        q -- Full-text search query string.

        :param q:
        :param kwargs:
        :return: responce (json)
        """
        pass
