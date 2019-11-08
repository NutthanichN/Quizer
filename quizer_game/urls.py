from django.urls import path

from . import views


urlpatterns = [
    # /quizer/
    path('', views.test_index, name='test_index'),
    # /quizer/game/1/
    # path('game/<int:quiz_id>/<int:player_id>/', views.game, name='game'),
    # /quizer/game/player-name/
    path('test-player-name/', views.run_test_player_name_template, name='test-player-name'),
    # /quizer/game/player-name/select-quiz/
    path('test-select-quiz/<str:player_name>/', views.run_test_select_quiz_template, name='test-select-quiz'),
    # /quizer/game/player_id/quiz_id/difficulty/question_id/
    path('start-game/<str:player_name>/<int:quiz_id>/<int:selected_difficulty>/<int:question_id>/',
         views.start_game, name='start-game'),
]

# player_name, quiz_id, selected_difficulty