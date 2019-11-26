from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from django.views import View
from django.contrib import messages



from .models import Quiz,Player,Question
# from .forms import QuizModelForm,QuestionModelForm



# Create your views here.
DIFFICULTY = {'easy': 0, 'medium': 1, 'hard': 2}
CHOICE_VALUE = {'wrong': 0, 'correct': 1}
POSITION = {'max': 15, 'min': 0}


def create_player(quiz, player_name, selected_difficulty):
    player = quiz.player_set.create(name=player_name)
    player.current_question = quiz.question_set.get(number=1)
    player.selected_difficulty = selected_difficulty
    player.is_playing = True
    player.save()
    return player


def setup_player_for_testing(quiz, player_name, selected_difficulty, position):
    player = quiz.player_set.get(name=player_name)
    player.current_question = quiz.question_set.get(number=1)
    player.position = position
    player.selected_difficulty = selected_difficulty
    player.save()
    return player


def index(request):
    return HttpResponse("Hello, world. You're at the Quizer game test index.")


def player_name(request):
    return render(request, 'quizer_game/player-name.html')


# <str:player_name>/quiz-level/
def quiz_level(request, player_name):
    context = {'player_name': player_name}
    return render(request, 'quizer_game/question-level.html', context)


# /quizer/start-game/player_name/quiz_id/difficulty/
def start_game(request, player_name, quiz_id, selected_difficulty):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    # test with existing player
    player = setup_player_for_testing(quiz, player_name, DIFFICULTY['easy'], POSITION['min'])

    # (real) create new player
    # player = create_player(quiz, player_name, selected_difficulty)

    return redirect(reverse('quizer_game:game',
                            kwargs={'player_id': player.id, 'quiz_id': quiz.id,
                                    'selected_difficulty': player.selected_difficulty, }
                            )
                    )


# /quizer/game/player_id/quiz_id/difficulty/
def game(request, player_id, quiz_id, selected_difficulty):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    player = quiz.player_set.get(pk=player_id)
    question = player.current_question
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
            player.is_failed = True
            player.is_playing = False
            player.save()
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


# /quizer/create-quiz/
def create_quiz(request):
    template_name = 'quizer_game/create-question.html'
    return render(request, template_name)


# /quizer/create-quiz/update/
def update_create_quiz(request):
    quiz_topic = request.POST.get('quiz_topic')
    quiz = Quiz(topic=quiz_topic)
    quiz.save()
    count_question = 0
    count_choice = 0

    # update question text from input
    for i in range(1, 21):
        question_text = request.POST.get(f'question_text_{i}')

        # check that user set question text
        if len(question_text) != 0:
            count_question = count_question + 1
        question = quiz.question_set.create(text=question_text, number=i)

        # update choice text from input
        for j in range(1, 5):
            choice_text = request.POST[f'{i}_choice_text_{j}']

            # check that user set choice text
            if len(choice_text) != 0:
                count_choice = count_choice  + 1
            choice_value = request.POST[f'{i}_choice_value']
            choice = question.choice_set.create(text=choice_text)

            # check the right choice
            if choice_value == f"choice{j}":
                choice.value = 1
                choice.save()

    # check that user set 20 questions and 80 choices
    if count_question == 20 and count_choice  == 80:
        messages.success(request, 'Successful saving')
        return redirect(reverse('quizer_game:create-question-set'))
    else:
        messages.error(request, 'Unsuccessful saving!! You must set 20 questions and 4 choices')
        quiz.delete()
        return redirect(reverse('quizer_game:create-question-set'))














