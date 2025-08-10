from django.urls import path
from . import views

urlpatterns = [
    path('watchlist/', views.WatchListView.as_view(), name='movie-list'),
    path('watchlist/<int:pk>/', views.WatchListDetailView.as_view(), name='movie-detail'),
    path('streaming-platforms/', views.StreamingPlatformView.as_view(), name='streaming-platform-list'),
    path('streaming-platforms/<int:pk>/', views.StreamingPlatformDetailView.as_view(), name='streaming-platform-detail'),
    path('reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    ]