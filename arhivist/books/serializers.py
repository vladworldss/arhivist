from rest_framework import serializers
from books.models import *

# class PublisherSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Publisher
#         fields = ('name', 'address', 'city',
#                   'state_province', 'country',
#                   'website'
#                   )
#
#
# class AuthorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#         fields = ('name', 'address', 'city',
#                   'state_province', 'country', 'website'
#                   )

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('publisher', 'description', 'language',
                  'published_date', 'title', 'page_count',
                  'canonical_volume_link', 'isbn_10', 'isbn_13',
                  'authors', 'categories', 'raw_title', 'path',
                  'validate', 'file_ext'
                  )