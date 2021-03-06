from django.urls import path

from . import views


app_name = 'quizer_game'
urlpatterns = [
    # /quizer/
    path('', views.index, name='index'),
    path('select-player-name/',
         views.player_name, name='player-name'),
    path('quiz-level/',
         views.quiz_level, name='quiz-level'),
    path('start-game/<str:player_name>/',
         views.start_game, name='start-game'),
    path('game/<int:player_id>/<int:quiz_id>/<int:selected_difficulty>/',
         views.game, name='game'),
    path('game/<int:player_id>/<int:quiz_id>/<int:selected_difficulty>/update/',
         views.update_game, name='update'),
    path('game/<int:player_id>/<int:quiz_id>/<int:selected_difficulty>/result/',
         views.result, name='result'),
    path('game/<int:player_id>/<int:quiz_id>/<int:selected_difficulty>/quit/',
         views.quit_game, name='quit-game'),
    path('game/<int:player_id>/<int:quiz_id>/<int:selected_difficulty>/<int:code>/upvote-downvote/',
         views.upvote_downvote, name='upvote-downvote'),
    path('leaderboard-index/',
         views.leaderboard_index, name='leaderboard-index'),
    path('leaderboard/<int:quiz_id>/<int:selected_difficulty>/',
         views.leaderboard, name='leaderboard'),
    path('login/',
         views.login, name='login'),
    path('create-quiz/',
         views.create_quiz, name='create-question-set'),
    path('create-quiz/update/',
         views.update_create_quiz, name='update_create_quiz'),
    path('edit-quiz/<int:quiz_id>/',
         views.edit_quiz, name='edit_quiz'),
    path('edit-quiz/<int:quiz_id>/update/',
         views.edit_data, name='edit_data'),
    path('quiz-index/',
         views.quiz_index, name='quiz-index'),
    path('user-profile/',
         views.user_profile, name='user_profile'),
    path('user-profile/update/',
         views.update_user_profile, name='update-user-profile'),
    path('logout/', views.logout_user, name='logout'),
    path('login-result/', views.login_result, name='login_result'),
]
