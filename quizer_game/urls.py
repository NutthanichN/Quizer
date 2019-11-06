from django.urls import path

from . import views


urlpatterns = [
    # /quizer/
    path('', views.test_index, name='test_index'),
    # /quizer/game/1/
    path('game/<int:quiz_id>', views.game, name='game'),
]
