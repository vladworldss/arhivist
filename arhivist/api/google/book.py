# coding: utf-8
"""
Interface for Google API.
"""
import os
import requests
import re
import json
import shutil
from apiclient.discovery import build

from arhivist.api.template import AbsBook
from .setting import API_KEY
from .deco import parsed

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class Book(AbsBook):
    """
    Google Books Api

    See: https://developers.google.com/books/
    """
    BASEURL = 'https://www.googleapis.com/books/v1'
    ID_THUMBNAIL = re.compile(r"http://[\w\./]*\?id=(?P<id>\w+)&\w+")

    def __init__(self, auth=True, **kw):
        self.authorized = False
        self.download_dir = kw.get('download_dir', '/var/www/api')
        if auth:
            books_service = build('books', 'v1', developerKey=API_KEY)
            self.volumes = books_service.volumes()
            self.authorized = True

    def _get(self, path, params=None):
        if params is None:
            params = {}
        resp = requests.get(self.BASEURL + path, params=params)
        if resp.status_code == 200:
            return json.loads(resp.content)

        return resp

    def get(self, volumeId, **kwargs):
        """Retrieves a Volume resource based on ID
        volumeId -- ID of volume to retrieve.
        Optional Parameters:
        partner --  Brand results for partner ID.

        projection -- Restrict information returned to a set of selected fields.
                    Acceptable values are:
                    "full" - Includes all volume data.
                    "lite" - Includes a subset of fields in volumeInfo and accessInfo.

        source --   String to identify the originator of this request.
        See: https://developers.google.com/books/docs/v1/reference/volumes/get
        """
        path = '/volumes/' + volumeId
        params = dict()
        for p in 'partner projection source'.split():
            if p in kwargs:
                params[p] = kwargs[p]

        return self._get(path)

    @parsed
    def list(self, q, **kwargs):
        """
        Performs a book search.
        q -- Full-text search query string.

            There are special keywords you can specify in the search terms to
            search in particular fields, such as:
            intitle: Returns results where the text following this keyword is
                    found in the title.
            inauthor: Returns results where the text following this keyword is
                    found in the author.
            inpublisher: Returns results where the text following this keyword
                    is found in the publisher.
            subject: Returns results where the text following this keyword is
                    listed in the category list of the volume.
            isbn:   Returns results where the text following this keyword is the
                    ISBN number.
            lccn:   Returns results where the text following this keyword is the
                    Library of Congress Control Number.
            oclc:   Returns results where the text following this keyword is the
                    Online Computer Library Center number.
        Optional Parameters:
        download -- Restrict to volumes by download availability.
                    Acceptable values are:
                    "epub" - All volumes with epub.
        filter --   Filter search results.
                    Acceptable values are:
                    "ebooks" - All Google eBooks.
                    "free-ebooks" - Google eBook with full volume text viewability.
                    "full" - Public can view entire volume text.
                    "paid-ebooks" - Google eBook with a price.
                    "partial" - Public able to see parts of text.
        langRestrict -- Restrict results to books with this language code.
        libraryRestrict	-- Restrict search to this user's library.
                    Acceptable values are:
                    "my-library" - Restrict to the user's library, any shelf.
                    "no-restrict" - Do not restrict based on user's library.
        maxResults -- Maximum number of results to return. Acceptable values are 0 to 40, inclusive.
        orderBy	 -- Sort search results.
                    Acceptable values are:
                    "newest" - Most recently published.
                    "relevance" - Relevance to search terms.
        partner	--  Restrict and brand results for partner ID.
        printType -- Restrict to books or magazines.
                    Acceptable values are:
                    "all" - All volume content types.
                    "books" - Just books.
                    "magazines" - Just magazines.
        projection -- Restrict information returned to a set of selected fields.
                    Acceptable values are:
                    "full" - Includes all volume data.
                    "lite" - Includes a subset of fields in volumeInfo and accessInfo.

        showPreorders -- Set to true to show books available for preorder. Defaults to false.
        source --  String to identify the originator of this request.
        startIndex -- Index of the first result to return (starts at 0)
        See: https://developers.google.com/books/docs/v1/reference/volumes/list
        """
        if self.authorized:
            res = self.volumes.list(q=q, **kwargs)
            return res.execute()

        path = '/volumes'
        params = dict(q=q)
        attrs = {'maxResults', 'showPreorders', 'langRestrict', 'libraryRestrict', 'download',
                 'printType', 'orderBy', 'startIndex', 'source', 'projection', 'partner', 'filter'
                 }

        common = attrs & set(kwargs)

        for p in common:
            params[p] = kwargs[p]

        return self._get(path, params)

    def title_list(self, q, **kwargs):
        q = f"intitle:{q}"
        return self.list(q, **kwargs)

    @staticmethod
    def get_thumbnail(url, w='w300'):
        """
        Save thumbnail from responce.

        :param url: thumbnail url
        like 'http://books.google.com/books/content?
                    id=junUDQAAQBAJ&
                    printsec=frontcover&
                    img=1&
                    zoom=1&
                    edge=curl&
                    source=gbs_api'

        :param w: weight
        :return:
        """
        url = '{}&fife={}'.format(url, w)
        return requests.get(url, stream=True)

    def get_id_thumbnail(self, url):
        match = self.ID_THUMBNAIL.match(url)
        if not match:
            raise Exception
        return match.groupdict()['id']

    @staticmethod
    def save_thumbnail(resp, path):
        """
        Save thumbnail.

        :param resp: responce from request
        :param path: path to save image
        :return:
        """
        with open(path, 'wb') as f:
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, f)

    def download_thumbnail(self, resp):
        t_url = resp['thumbnail']['url']
        t_id = self.get_id_thumbnail(t_url)

        t_resp = self.get_thumbnail(t_url)
        t_name = f"{t_id}.png"
        full_path = os.path.join(self.download_dir, t_name)
        self.save_thumbnail(t_resp, full_path)
        resp['thumbnail'] = t_name
