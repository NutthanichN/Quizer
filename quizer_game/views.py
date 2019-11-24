from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from django.views import View
from django.utils.datastructures import MultiValueDictKeyError



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



def create_quiz(request):
    template_name = 'quizer_game/create-question.html'
    return render(request, template_name)



def update_data(request):
    quiz_topic = request.POST.get('quiz_topic')
    # question_text = request.POST.get('question_text')
    # choice_text = request.POST.get('choice_text')
    quiz = Quiz(topic=quiz_topic)
    quiz.save()




    # question = quiz.question_set.create(text=question_text)
    # choice = question.choice_set.create(text=choice_text)



    # question_text = request.POST['question_text']

    try:


        for i in range(1, 3):
            question_text = request.POST[f'question_text_{i}']
            question = quiz.question_set.create(text=question_text,number=i)
            question.save()


            for j in range(1,5):
                choice_text = request.POST[f'{i}_choice_text_{j}']
                choice = question.choice_set.create(text=choice_text)
                choice.save()



    except MultiValueDictKeyError:
        print("add question until 20")

    return redirect(reverse('quizer_game:create-question-set'))


#
#
# class UpadateCreatequiz(View):
#
#     def get(self,request,player_id,quiz_id,*args, **kwargs):
#         form_quiz = QuizModelForm()
#         quiz = get_object_or_404(Quiz, pk=quiz_id)
#         player = quiz.player_set.get(pk=player_id)
#         return redirect(reverse('quizer_game:create-question-set', kwargs={'player_id': player.id,'quiz_id': quiz.id}))
#
#     def post(self,request,player_id,quiz_id,*args, **kwargs):
#         form_quiz = QuizModelForm(request.POST)
#         quiz = get_object_or_404(Quiz, pk=quiz_id)
#         player = quiz.player_set.get(pk=player_id)
#         if form_quiz.is_valid():
#             form_quiz.save()
#         return redirect(reverse('quizer_game:create-question-set',kwargs={'player_id': player.id,'quiz_id': quiz.id}))


# class Createquiz(View):
#     template_name = 'quizer_game/create-question.html'
#
#     def get(self, request,*args, **kwargs):
#         form_quiz = QuizModelForm()
#         text = Question.objects.create(quiz = Quiz)
#         form_question = QuestionModelForm(instance=text)
#         # title = self.cleaned_data.get('topic')
#         #
#         # form = QuestionForm(request.POST or None)
#         # if request.method == "POST":
#         #     if form.is_valid():
#         #         question = form.cleaned_data.get('question')
#         #         number_of_answers = form.cleaned_data.get('number_of_answers')
#         #         create_question = Question.objects.create(question=question, number_of_answers=number_of_answers)
#         #         create_question.save()
#         #         return redirect('home:add-answers', id=create_question.id)
#         # return render(request, 'home/add_question.html', {'form': form})
#
#         # form_choice = ChoiceModelForm()
#         # quiz = get_object_or_404(Quiz, pk=quiz_id)
#         # quiz = Quiz.objects.create(topic=form_quiz)
#         # player = quiz.player_set.create(name=player_name)
#
#         # player.current_question =  quiz.question_set.get(number=new_question_number)
#         # player = Player(pk=player_id)
#         # old_question = player.current_question
#         # new_question_number = old_question.number + 1
#         # player.current_question = quiz.question_set.get(number=new_question_number)
#         # form_question = QuestionModelForm(instance=player.current_question)
#         context = {'form_quiz': form_quiz,'form_question': form_question}
#         return render(request, self.template_name, context)
#
#     def post(self, request, *args, **kwargs):
#         form_quiz = QuizModelForm(request.POST)
#         text = Question.objects.create(quiz= )
#         form_question = QuestionModelForm(request.POST, instance=text)
#
#
#         # form_question = QuestionModelForm(id=form_quiz.id)
#
#         # quiz = get_object_or_404(Quiz, pk=quiz_id)
#         # player = quiz.player_set.get(pk=player_id)
#         # old_question = player.current_question
#         # new_question_number = old_question.number + 1
#         # player.current_question = quiz.question_set.get(number=new_question_number)
#         # form_question = QuestionModelForm(request.POST, instance = player.current_question)
#         if form_quiz.is_valid():
#             form_quiz.save()
#
#         if form_question.is_valid():
#             form_question.save()
#
#         context = {'form_quiz': form_quiz, 'form_question': form_question}
#         return render(request, self.template_name, context)
#
#
#




