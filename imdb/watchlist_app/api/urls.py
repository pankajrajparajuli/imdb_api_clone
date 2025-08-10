from django.urls import path
from . import views

urlpatterns = [
    path('watchlist/', views.MovieListView.as_view(), name='movie-list'),
    path('watchlist/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
]