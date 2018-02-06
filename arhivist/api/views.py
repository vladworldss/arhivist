from django.shortcuts import render
from django.http.response import HttpResponse
# Create your views here.

def api_doc(request, *args, **kw):
    return HttpResponse("Arhivist api")
