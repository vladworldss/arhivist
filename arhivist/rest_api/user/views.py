# coding: utf-8
"""
Views for user-rest-api.
"""

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.generics import (
    CreateAPIView, ListAPIView
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from rest_framework_jwt.settings import api_settings

from .serializers import UserSerializer


class UserList(ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class CreateUserView(CreateAPIView):

    model = User.objects.all()
    # Or anon users can't register
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = self.model.get(username=serializer.data['username'])
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        data = {'confirmation_url': reverse('activate-user', args=[token], request=request)}
        return Response(data=data, status=status.HTTP_201_CREATED, headers=headers)
