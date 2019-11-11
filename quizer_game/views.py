from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from .models import Quiz

# Create your views here.
DIFFICULTY = {'easy': 0, 'medium': 1, 'hard': 2}
CHOICE_VALUE = {'wrong': 0, 'correct': 1}
POSITION = {'max': 15, 'min': 0}


def test_index(request):
    return HttpResponse("Hello, world. You're at the Quizer game test index.")


# /quizer/start-game/player_name/quiz_id/difficulty/
def start_game(request, player_name, quiz_id, selected_difficulty):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    # test with player 1
    player = setup_player_for_testing(quiz, player_name, DIFFICULTY['easy'], POSITION['min'])

    # (real) create new player
    # player = quiz.create_player(player_name, selected_difficulty)

    return redirect(reverse('quizer_game:game',
                            kwargs={'player_id': player.id, 'quiz_id': quiz.id,
                                    'selected_difficulty': player.selected_difficulty,
                                    }
                            )
                    )


def setup_player_for_testing(quiz, player_name, selected_difficulty, position):
    player = quiz.player_set.get(name=player_name)
    player.current_question = quiz.question_set.get(number=1)
    player.position = position
    player.selected_difficulty = selected_difficulty
    player.save()
    return player


# /quizer/game/player_id/quiz_id/difficulty/
def game(request, player_id, quiz_id, selected_difficulty):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    player = quiz.player_set.get(pk=player_id)
    question = player.current_question
    # question = quiz.question_set.get(pk=1)
    context = {'quiz': quiz,
               'player': player,
               'question': question,
               }
    return render(request, 'quizer_game/game.html', context)


# TODO edit redirect to the real template
# TODO manage player time spent and set limit time for the hard level
# TODO provide upvote-downvote feature
# /quizer/game/player_id/quiz_id/difficulty/update/
def update_game(request, player_id, quiz_id, selected_difficulty, choice_value):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    player = quiz.player_set.get(pk=player_id)

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
        try:
            old_question = player.current_question
            new_question_number = old_question.number + 1
            player.current_question = quiz.question_set.get(number=new_question_number)
        except ObjectDoesNotExist:
            player.is_failed = True
            player.is_playing = False
            player.save()
            return redirect(reverse('quizer_game:test-result-fail'))

    player.save()
    return redirect(reverse('quizer_game:game',
                            kwargs={'player_id': player.id, 'quiz_id': quiz.id,
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

