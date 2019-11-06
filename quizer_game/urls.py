from django.urls import path

from . import views


urlpatterns = [
    path('', views.test_index, name='test_index'),
    # path('game/', views)
]
