from django.urls import path

from . import views


app_name = 'quizer_game'
urlpatterns = [
    # /quizer/
    path('', views.index, name='index'),
    path('select-player-name/', views.player_name, name='player-name'),
    path('quiz-level/', views.quiz_level, name='quiz-level'),
    path('start-game/<str:player_name>/',
         views.start_game, name='start-game'),
    # /quizer/game/player_id/quiz_id/difficulty/question_id/
    path('game/<int:player_id>/<int:quiz_id>/<int:selected_difficulty>/',
         views.game, name='game'),
    # /quizer/game/player_id/quiz_id/difficulty/choice_value/update/
    path('game/<int:player_id>/<int:quiz_id>/<int:selected_difficulty>/update/',
         views.update_game, name='update'),
    path('game/<int:player_id>/<int:quiz_id>/<int:selected_difficulty>/result/',
         views.result, name='result'),
    # /quizer/game/player_id/quiz_id/difficulty/choice_value/
    path('create-quiz/',
         views.create_quiz, name='create-question-set'),
    path('create-quiz/update/',
         views.update_create_quiz, name='update_create_quiz'),
    path('edit-quiz/<int:quiz_id>/',
         views.edit_quiz, name='edit_quiz'),
    path('edit-quiz/<int:quiz_id>/update/',
         views.edit_data, name='edit_data'),
]
