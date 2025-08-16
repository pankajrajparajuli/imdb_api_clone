from django.urls import path
from . import views

urlpatterns = [
    path('', views.WatchListView.as_view(), name='movie-list'),
    path('<int:pk>/', views.WatchListDetailView.as_view(), name='movie-detail'),
    path('search/', views.SearchWatchListView.as_view(), name='search-list'),
    
    path('streaming-platforms/', views.StreamingPlatformView.as_view(), name='streaming-platform-list'),
    path('streaming-platforms/<int:pk>/', views.StreamingPlatformDetailView.as_view(), name='streaming-platform-detail'),
    
    path('<int:pk>/reviews-create/', views.ReviewCreateView.as_view(), name='review-create'),
    path('<int:pk>/reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    path('reviews/user/', views.UserReviewDetailView.as_view(), name='user-reviews'),
    ]