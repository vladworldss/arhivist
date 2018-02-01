# coding: utf-8
import abc


class AbsApi(metaclass=abc.ABCMeta):
    """
    Abstract base class for search book with api
    """

    # @abc.abstractmethod
    def get(self, volume_id, **kwargs):
        """
        Retrieves a Volume resource based on ID
        volume_id -- ID of volume to retrieve.

        :param volume_id:
        :param kwargs:
        :return: responce (json)
        """
        raise NotImplementedError

    # @abc.abstractmethod
    def list(self, q, **kwargs):
        """
        Performs a volume search.
        q -- Full-text search query string.

        :param q:
        :param kwargs:
        :return: responce (json)
        """
        raise NotImplementedError

    # @abc.abstractmethod
    def authorize(self, *args, **kw):
        """
        Authorization of client.

        :param args:
        :param kw:
        :return:
        """
        raise NotImplementedError

    def make_bad_responce(self, *args, **kw):
        """
        Authorization of client.

        :param args:
        :param kw:
        :return:
        """
        raise NotImplementedError


class AbsBookApi(AbsApi):

    # @abc.abstractmethod
    def get_book(self, book_id):
        """
        Get a Book resource based on ID.

        :param book_id:
        :return:
        """
        raise NotImplementedError

    # @abc.abstractmethod
    def search_book(self, *args, **kw):
        """


        :param args:
        :param kw: title
        :return:
        """
        raise NotImplementedError

    def post_book(self, book):
        """

        :param book:
        :return:
        """
        raise NotImplementedError

    def delete_book(self, book):
        raise NotImplementedError

    # @abc.abstractmethod
    def download_thumbnail(self, link, download_dir):
        raise NotImplementedError
