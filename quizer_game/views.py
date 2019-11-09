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
    player.position = 11
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


DIFFICULTY = {'easy': 0, 'medium': 1, 'hard': 2}
CHOICE_VALUE = {'wrong': 0, 'correct': 1}
POSITION = {'max': 15, 'min': 0}
QUESTION_NUM = {'max': 20}


# TODO edit redirect to the real template
# TODO manage player time spent and set limit time for the hard level
# TODO provide upvote-downvote feature
# TODO manage admit page (so we don't have to create quiz by API)
# /quizer/game/player_id/quiz_id/difficulty/update/
def update_game(request, player_id, quiz_id, selected_difficulty, choice_value):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    player = quiz.player_set.get(pk=1)

    # update position
    if choice_value == CHOICE_VALUE['correct']:
        if player.position < POSITION['max']:
            player.move_forward()
    else:
        if selected_difficulty > DIFFICULTY['easy']:
            if player.position > POSITION['min']:
                player.move_backward()

    if player.position == POSITION['max']:
        player.is_achieved = True
        player.is_playing = False
        player.save()
        return redirect(reverse('quizer_game:test-result-achieve'))
    elif player.position < POSITION['max']:
        # change to next question
        if player.current_question.number < QUESTION_NUM['max']:
            old_question = player.current_question
            new_question_number = old_question.number + 1
            player.current_question = quiz.question_set.get(number=new_question_number)
        # check when question num = 20 but player doesn't reach the finish line
        elif player.current_question.number == QUESTION_NUM['max']:
            player.is_failed = True
            player.is_playing = False
            player.save()
            return redirect(reverse('quizer_game:test-result-fail'))

    player.save()
    return redirect(reverse('quizer_game:game',
                            kwargs={'player_id': 1, 'quiz_id': quiz_id,
                                    'selected_difficulty': selected_difficulty}))


def render_test_result_achieve(request):
    return render(request, 'quizer_game/test-result-achieve.html')


def render_test_result_fail(request):
    return render(request, 'quizer_game/test-result-fail.html')


def render_test_select_quiz_template(request, player_name):
    context = {'player_name': player_name}
    return render(request, 'quizer_game/test-select-quiz.html', context)


def render_test_player_name_template(request):
    return render(request, 'quizer_game/test-player-name.html')

