# coding: utf-8
"""
Json-serializers for user-rest-api.
"""
from django.contrib.auth.models import User
from rest_framework.serializers import (
    ModelSerializer, PrimaryKeyRelatedField
)

from books.models import Book


class UserSerializer(ModelSerializer):
    """
    User sezializer class.
    """
    books = PrimaryKeyRelatedField(many=True, queryset=Book.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'books')

    def create(self, validated_data):
        user = User(email=validated_data['email'],
                    username=validated_data['username']
                    )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user
