from django.urls import path
from . import views

urlpatterns = [
    path('watchlist/', views.watchlist, name='watchlist'),
]