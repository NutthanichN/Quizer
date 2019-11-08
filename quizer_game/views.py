from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from .models import Quiz

# Create your views here.


def test_index(request):
    return HttpResponse("Hello, world. You're at the Quizer game test index.")


# def game(request, quiz_id):
#     quiz = get_object_or_404(Quiz, pk=quiz_id)
#     return render(request, 'quizer_game/game.html',
#                   {'quiz': quiz})
#     # response = "Game of Quiz %s."
#     # return HttpResponse(response % quiz_id)

# class GameView()

# /quizer/game/player_name/quiz_id/difficulty/question_id/
def start_game(request, player_name, quiz_id, selected_difficulty, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    # test with player 1
    player = quiz.player_set.get(pk=1)
    # create new player
    # player = quiz.create_player(player_name, selected_difficulty)
    # player = quiz.player_set.create(name='player2', selected_difficulty=0, is_playing=True)
    question = quiz.question_set.get(pk=question_id)
    context = {'quiz': quiz,
               'player': player,
               'question': question,
               }
    return render(request, 'quizer_game/game.html', context)


def run_test_select_quiz_template(request, player_name):
    context = {'player_name': player_name}
    return render(request, 'quizer_game/test-select-quiz.html', context)


def run_test_player_name_template(request):
    return render(request, 'quizer_game/test-player-name.html')


def answer(request):
    pass
