from django.contrib.auth.models import User
from rest_framework import serializers

from books.models import Book


class BookSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Book
        fields = ('publisher', 'description', 'language',
                  'published_date', 'title', 'page_count',
                  'canonical_volume_link', 'isbn_10', 'isbn_13',
                  'authors', 'categories', 'raw_title', 'path',
                  'validate', 'file_ext', 'owner'
                  )


class UserSerializer(serializers.ModelSerializer):
    books = serializers.PrimaryKeyRelatedField(many=True, queryset=Book.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'books')
