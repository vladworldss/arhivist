from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from books.views import book_list


urlpatterns = [
    url(r'^books/$', book_list),
    # url(r'^books/(?P<pk>[0-9]+)/$', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)