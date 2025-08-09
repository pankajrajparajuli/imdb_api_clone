from django.urls import path
from . import views

urlpatterns = [
    path('watchlist/', views.movie_list, name='movie-list'),
    path('watchlist/<int:pk>/', views.movie_detail, name='movie-detail'),
]