from django.urls import path

from . import views


app_name = 'quizer_game'
urlpatterns = [
    # /quizer/
    path('', views.test_index, name='test_index'),

    # /quizer/game/player-name/
    path('test-player-name/', views.render_test_player_name_template, name='test-player-name'),

    # /quizer/game/player-name/select-quiz/
    path('test-select-quiz/<str:player_name>/', views.render_test_select_quiz_template, name='test-select-quiz'),

    path('start-game/<str:player_name>/<int:quiz_id>/<int:selected_difficulty>/',
         views.start_game, name='start-game'),

    # /quizer/game/player_id/quiz_id/difficulty/question_id/
    path('game/<int:player_id>/<int:quiz_id>/<int:selected_difficulty>/',
         views.game, name='game'),

    # /quizer/game/player_id/quiz_id/difficulty/choice_value/update/
    path('game/<int:player_id>/<int:quiz_id>/<int:selected_difficulty>/<int:choice_value>/update/',
         views.update_game, name='update'),

    # /quizer/game/test-result/
    path('game/test-result-achieve', views.render_test_result_achieve, name='test-result-achieve'),
    path('game/test-result-fail', views.render_test_result_fail, name='test-result-fail'),
]
