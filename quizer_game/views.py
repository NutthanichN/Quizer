from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from .models import Quiz

# Create your views here.


def test_index(request):
    return HttpResponse("Hello, world. You're at the Quizer game test index.")


def game(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'quizer_game/game.html',
                  {'quiz': quiz})
    # response = "Game of Quiz %s."
    # return HttpResponse(response % quiz_id)

# class GameView()


def answer(request):
    pass
