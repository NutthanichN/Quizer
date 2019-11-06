from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def test_index(request):
    return HttpResponse("Hello, world. You're at the Quizer game test index.")


# def game(request):
#     return
