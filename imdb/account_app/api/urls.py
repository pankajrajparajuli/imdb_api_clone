from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/', obtain_auth_token, name='api-login'),
    path('register/', views.register, name='api-register'),
    path('logout/', views.logout, name='api-logout'),
]
