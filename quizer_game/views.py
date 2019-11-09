from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from .models import Quiz

# Create your views here.


def test_index(request):
    return HttpResponse("Hello, world. You're at the Quizer game test index.")


# /quizer/start-game/player_name/quiz_id/difficulty/
def start_game(request, player_name, quiz_id, selected_difficulty):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    # questions = list(quiz.question_set.all())
    # test with player 1
    player = quiz.player_set.get(pk=1)
    player.current_question = quiz.question_set.get(number=1)
    # player.selected_difficulty = selected_difficulty
    player.save()
    # create new player
    # player = quiz.create_player(player_name, selected_difficulty)

    return redirect(reverse('quizer_game:game',
                            kwargs={'player_id': 1, 'quiz_id': quiz_id,
                                    'selected_difficulty': selected_difficulty,
                                    }))


# /quizer/game/player_id/quiz_id/difficulty/
def game(request, player_id, quiz_id, selected_difficulty):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    player = quiz.player_set.get(pk=1)
    question = player.current_question
    # question = quiz.question_set.get(pk=1)
    context = {'quiz': quiz,
               'player': player,
               'question': question,
               }
    return render(request, 'quizer_game/game.html', context)


# /quizer/game/player_id/quiz_id/difficulty/update/
def update_game(request, player_id, quiz_id, selected_difficulty, choice_value):
    # game difficulty: easy(0) medium(1) hard(2)
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    player = quiz.player_set.get(pk=1)

    if selected_difficulty == 0:
        if choice_value > 0:
            player.move_forward()
    else:
        if choice_value > 0:
            player.move_forward()
        else:
            player.move_backward()
    player.save()

    return redirect(reverse('quizer_game:game',
                            kwargs={'player_id': 1, 'quiz_id': quiz_id,
                                    'selected_difficulty': selected_difficulty}))


def run_test_select_quiz_template(request, player_name):
    context = {'player_name': player_name}
    return render(request, 'quizer_game/test-select-quiz.html', context)


def run_test_player_name_template(request):
    return render(request, 'quizer_game/test-player-name.html')

