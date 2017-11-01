from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from books.views import BooksList, UserList


urlpatterns = [
    url(r'^books/$', BooksList.as_view()),
    url(r'^users/$', UserList.as_view()),

    # url(r'^books/(?P<pk>[0-9]+)/$', views.books_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)

