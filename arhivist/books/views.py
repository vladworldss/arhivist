import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from books.models import *
from books.serializers import BookSerializer


def get_publisher(request=None):
    if not request:
        return Publisher.make(name='test_publisher')
    return Publisher.make(name=request.POST['publisher'])


def get_lang(request=None):
    if not request:
        return Language.make(name='test_lang')
    return Language.make(name=request.POST['language'])


def post_update(request, publisher, language):
    request.POST._mutable = True

    request.POST.update({'publisher': publisher,
                         'language': language,
                         })


def get_author_names(request=None):
    if not request:
        return ['tanya', 'vova']
    authors_names = request.POST.getlist('authors')
    request.POST.pop('authors')
    return authors_names


def get_categories_names(request=None):
    if not request:
        return ['home', 'video']
    categories_names = request.POST.getlist('categories')
    request.POST.pop('categories')
    return categories_names


@api_view(['GET', 'POST'])
def book_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    try:
        publisher = get_publisher(request)
        language = get_lang(request)
        post_update(request, publisher, language)
        authors_names = get_author_names(request)
        categories_names = get_categories_names(request)

        try:
            book = Book.make(**request.POST.dict())
            for a in authors_names:
                auth = Author.make(name=a)
                book.authors.add(auth)

            for c in categories_names:
                cat = Categories.make(name=c)
                book.categories.add(cat)
            book.save()

        except Exception as e:
            return Response(str(e))

        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)



# class BooksList(generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#
#     def post(self, request, *args, **kwargs):
#         try:
#             publisher = Publisher.make(name=request.POST['publisher'])
#             language = Language.make(name=request.POST['language'])
#             request.POST._mutable = True
#
#             request.POST.update({'publisher': publisher,
#                                  'language': language,
#                                  'path': '/home/test/',
#                                  'raw_title': 'xxx'
#                                  })
#             authors_names = request.POST.getlist('authors')
#             request.POST.pop('authors')
#             categories_names = request.POST.getlist('categories')
#             request.POST.pop('categories')
#             test_conf = {'publisher': publisher,
#                          'description': '',
#                          'language': language,
#                          'published_date': '2005-01-01',
#                          'title': 'How to Live Like You Were Dying- PDF',
#                          'page_count': '0',
#                          'canonical_volume_link': 'https://books.google.com/books/about/How_to_Live_Like_You_Were_Dying_PDF.html?hl=&id=gNFcTw52DPUC',
#                          'path': '/home/test/',
#                          'raw_title': 'xxx'
#                          }
#             try:
#                 book = Book.objects.create(**test_conf)
#             except Exception as e:
#                 return Response(e)
#
#             for a in authors_names:
#                 Author.objects.create(book=book, name=a)
#
#             for c in categories_names:
#                 Categories.objects.create(book=book, name=c)
#
#             serializer = BookSerializer(book)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response(e, status=status.HTTP_400_BAD_REQUEST)
