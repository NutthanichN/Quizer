from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import Quiz, Choice, Timer

from datetime import timedelta
import time

# Create your views here.
DIFFICULTY = {'easy': 0, 'medium': 1, 'hard': 2}
DIFFICULTY_NUM = {0: 'Easy', 1: 'Medium', 2: 'Hard'}
CHOICE_VALUE = {'wrong': 0, 'correct': 1}
POSITION = {'max': 15, 'min': 0}
HARD_LVL_TIME_LIMIT = 60            # seconds


def create_player(quiz, player_name, selected_difficulty):
    player = quiz.player_set.create(name=player_name)
    player.timer_set.create()
    player.current_question = quiz.question_set.get(number=1)
    player.selected_difficulty = selected_difficulty
    player.is_playing = True
    player.save()
    return player


def setup_timer(player):
    # setup default values to timer
    timer = Timer.objects.get(player=player)
    if player.selected_difficulty == DIFFICULTY['hard']:
        timer.set_time_limit(seconds=HARD_LVL_TIME_LIMIT)

    # for testing
    timer.start_point = timedelta(seconds=int(time.time()))
    timer.end_point = timedelta(seconds=int(time.time()))

    timer.save()
    return timer


def setup_player_for_testing(quiz, player_name, selected_difficulty, position):
    # setup default values to player
    player = quiz.player_set.get(name=player_name)
    player.current_question = quiz.question_set.get(number=1)
    player.position = position
    player.selected_difficulty = selected_difficulty
    player.correct_answer = 0
    player.wrong_answer = 0
    player.is_playing = True
    player.is_failed = False
    player.is_achieved = False
    player.is_timeout = False
    player.save()
    # setup default values to timer
    timer = Timer.objects.get(player=player)
    timer.start_point = timedelta(seconds=int(time.time()))
    timer.end_point = timedelta(seconds=int(time.time()))
    timer.save()

    return player


def index(request):
    # return HttpResponse("Hello, world. You're at the Quizer game test index.")
    return render(request, 'quizer_game/index.html')


def player_name(request):
    return render(request, 'quizer_game/player-name.html')


# <str:player_name>/quiz-level/
def quiz_level(request):
    input_player_name = request.POST['player_name']
    quizzes = Quiz.objects.all()
    context = {'player_name': input_player_name,
               'quizzes': quizzes}
    return render(request, 'quizer_game/question-level.html', context)


# /quizer/start-game/player_name/quiz_id/difficulty/
def start_game(request, player_name):
    quiz_id = request.POST['quiz_id']
    difficulty = request.POST['difficulty']
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    # test with existing player
    player = setup_player_for_testing(quiz, player_name, DIFFICULTY[difficulty], POSITION['min'])

    # uncomment this for real use
    # player = create_player(quiz, player_name, selected_difficulty)

    timer = setup_timer(player)
    timer.start()
    
    return redirect(reverse('quizer_game:game',
                            kwargs={'player_id': player.id, 'quiz_id': quiz.id,
                                    'selected_difficulty': player.selected_difficulty, }
                            )
                    )


# /quizer/game/player_id/quiz_id/difficulty/
# TODO handle error (link to 404 not found page)
def game(request, player_id, quiz_id, selected_difficulty):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    player = quiz.player_set.get(pk=player_id)
    question = player.current_question
    # timer = Timer.objects.get(player=player)
    context = {'quiz': quiz,
               'player': player,
               'question': question,
               'time_limit': HARD_LVL_TIME_LIMIT,
               }
    return render(request, 'quizer_game/game.html', context)


# TODO provide upvote-downvote feature
# TODO handle error (link to 404 not found page)
# /quizer/game/player_id/quiz_id/difficulty/update/
def update_game(request, player_id, quiz_id, selected_difficulty):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    player = quiz.player_set.get(pk=player_id)
    choice_id = request.POST['choice_id']
    choice = Choice.objects.get(pk=choice_id)
    timer = Timer.objects.get(player=player)
    timer.stop()

    # update position
    if choice.value == CHOICE_VALUE['correct']:
        player.correct_answer += 1
        if player.position < POSITION['max']:
            player.move_forward()
    else:
        player.wrong_answer += 1
        if selected_difficulty > DIFFICULTY['easy']:
            if player.position > POSITION['min']:
                player.move_backward()

    # check time for hard level
    # player can still play game but player won't be ranked on leaderboard
    # TODO prevent player from answering after time's up
    if selected_difficulty == DIFFICULTY['hard']:
        if timer.time_duration >= timer.time_limit:
            player.is_timeout = True
            player.save()

    # check if player reaches the finish line or not
    if player.position == POSITION['max']:
        if not player.is_timeout:
            player.is_achieved = True
        player.is_playing = False
        player.save()
        player.save_time_duration()
        return redirect(reverse('quizer_game:result',
                                kwargs={'player_id': player.id, 'quiz_id': quiz.id,
                                        'selected_difficulty': player.selected_difficulty, }
                                )
                        )
    elif player.position < POSITION['max']:
        # change to next question
        try:
            old_question = player.current_question
            new_question_number = old_question.number + 1
            player.current_question = quiz.question_set.get(number=new_question_number)
        except ObjectDoesNotExist:
            if not player.is_timeout:
                player.is_failed = True
            player.is_playing = False
            player.save()
            player.save_time_duration()
            return redirect(reverse('quizer_game:result',
                                    kwargs={'player_id': player.id, 'quiz_id': quiz.id,
                                            'selected_difficulty': player.selected_difficulty, }
                                    )
                            )

    player.save()
    return redirect(reverse('quizer_game:game',
                            kwargs={'player_id': player.id, 'quiz_id': quiz.id,
                                    'selected_difficulty': selected_difficulty}
                            )
                    )


# game/<int:player_id>/<int:quiz_id>/<int:selected_difficulty>/result/
def result(request, player_id, quiz_id, selected_difficulty):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    player = quiz.player_set.get(pk=player_id)
    context = {'quiz': quiz, 'player': player}
    return render(request, 'quizer_game/result.html', context)


def leaderboard_index(request):
    quiz = Quiz.objects.all()
    context = {'quizzes': quiz}
    return render(request, 'quizer_game/leaderboard-index.html', context)


def login(request):
    return render(request, 'quizer_game/login.html')


def leaderboard(request, quiz_id, selected_difficulty):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    players = quiz.player_set.filter(selected_difficulty=selected_difficulty,
                                     is_achieved=True)
    players.order_by('time')
    # number = range(1, player.id+1)
    context = {'quiz': quiz,
               'players': players,
               'difficulty': DIFFICULTY_NUM[selected_difficulty],
               }
    return render(request, 'quizer_game/leaderboard.html', context)
