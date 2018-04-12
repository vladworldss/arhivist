# Arhivist 
Arhivist is a web application based on [Django](https://www.djangoproject.com).
Also, it's supported REST web services based on [Django REST framework](http://www.django-rest-framework.org) with Authentication policies for [JSON Web Tokens](https://jwt.io/).
The actual code of the app implements a store of books application with tests, demo project and documentation.

## Example
We can get a json of the books. We use Paginator for getting of part of all objects.

```http http://127.0.0.1:8000/api/books/```
```HTTP/1.0 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 2168
Content-Type: application/json
Date: Wed, 27 Dec 2017 14:48:38 GMT
Server: WSGIServer/0.2 CPython/3.6.2
Vary: Accept
X-Frame-Options: SAMEORIGIN
   
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "owner": "admin",
            "description": "Would I Lie to You? Not This Year. Veteran author and speaker ...",
            "published_date": "2005-01-01",
            "title": "How to Live Like You Were Dying",
            "page_count": 10,
            "canonical_volume_link": "https://books.google.com/books/about/How_to_Live_Like_You_Were_Dying_PDF.html?hl=&id=gNFcTw52DPUC",
            "isbn_10": 976891212,
            "isbn_13": 9780976891215,
            "thumbnail": "",
            "path": "/home/test/",
            "raw_title": "How to Live Like You Were Dyin",
            "file_ext": "",
            "validate": false,
            "publisher": 1,
            "language": 1,
            "author": [
                1
            ],
            "category": [
                1
            ]
        },
        {
            "id": 2,
            "owner": "admin",
            ...
        }
    ]
}
```

### Prerequisites
What things you need to install the software and how to install them
```
git
CPython 3.6.x
pip, virtualenv or pyenv
```
### Installing
I prefere pyenv.
```
$ pyenv virtualenv 3.6.2 arhivist
$ pyenv local arhivist && pip install --upgrade pip
$ pip install wheel
$ git clone https://github.com/vladworldss/arhivist.git && cd arhivist
$ pip install -r requirements.txt
```

### Run
Default store folder == "/home/test/books". For another folder please change arhivist/parser/settings.py::STORE_PATH.
Default credentials for superuser - "api.settings".
```
$ cd arhivist
$ python manage.py createsuperuser
$ python manage.py makemigrations
$ python migrate
$ nohup manage.py runserver 0.0.0.0:8000
$ cd parser &&  python store.py -i --vendor google
```