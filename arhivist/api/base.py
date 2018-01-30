import os
import shutil
import requests

from .template import AbsBookApi


class BaseBookApi(AbsBookApi):

    BASE_URL = None

    def __init__(self, auth=True, **kw):
        self.authorized = False
        self.choiser = None
        if auth:
            self.authorize()

    def download_thumbnail(self, url, download_dir):
        return self.ThumbnailApi.download(url, download_dir)

    class ThumbnailApi(object):
        """
        Thumbnail Api base class.
        """

        @classmethod
        def download(cls, url, download_dir):
            t_name = cls.get_thumbnail_name(url)
            t_resp = cls.get_thumbnail(url)
            cls.save_thumbnail(t_resp, download_dir, t_name)
            return t_name

        @classmethod
        def get_thumbnail_name(cls, url):
            raise NotImplementedError

        @classmethod
        def get_thumbnail(cls, url, weight='w300'):
            """
            Save thumbnail from responce.

            :param url: thumbnail url
            :param str w: weight
            :return: stream-responce
            """
            scale_url = cls.make_scale_url(url, weight)
            return requests.get(scale_url, stream=True)

        @classmethod
        def make_scale_url(cls, url, weight):
            raise NotImplementedError

        @staticmethod
        def save_thumbnail(stream_resp, download_dir, file_name):
            """
            Save thumbnail.

            :param responce stream_resp: raw responce
            :param download_dir: path to directory
            :param str file_name: name of thumbnail
            :return:
            """
            full_path = os.path.join(download_dir, file_name)
            with open(full_path, 'wb') as f:
                stream_resp.raw.decode_content = True
                shutil.copyfileobj(stream_resp.raw, f)
            return full_path
