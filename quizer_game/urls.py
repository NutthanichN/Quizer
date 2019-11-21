from django.urls import path

from . import views
from .views import UpadateCreatequiz


app_name = 'quizer_game'
urlpatterns = [
    # /quizer/
    path('', views.index, name='index'),
    path('select-player-name/', views.player_name, name='player-name'),
    path('<str:player_name>/quiz-level/', views.quiz_level, name='quiz-level'),
    path('start-game/<str:player_name>/<int:quiz_id>/<int:selected_difficulty>/',
         views.start_game, name='start-game'),
    # /quizer/game/player_id/quiz_id/difficulty/question_id/
    path('game/<int:player_id>/<int:quiz_id>/<int:selected_difficulty>/',
         views.game, name='game'),
    # /quizer/game/player_id/quiz_id/difficulty/choice_value/update/
    path('game/<int:player_id>/<int:quiz_id>/<int:selected_difficulty>/<int:choice_value>/update/',
         views.update_game, name='update'),
    path('game/<int:player_id>/<int:quiz_id>/<int:selected_difficulty>/result/',
         views.result, name='result'),
    # path('create-question-set/<int:player_id>/<int:quiz_id>/',
    #      Createquiz.as_view(), name='create-question-set'),
    path('create-question-set/<int:player_id>/<int:quiz_id>/',
         views. create_quiz, name='create-question-set'),
    path('create-question-set/<int:player_id>/<int:quiz_id>/update/',
         UpadateCreatequiz.as_view(), name='update-create-question-set'),




]
