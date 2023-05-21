from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from transport import rfx


def index(request):
    rfx.switch_off("0120609:1")
    return HttpResponse("Hello, world. You're at the transport index.")
