from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', obtain_auth_token, name='api-login'),# Token authentication endpoint
    path('register/', views.register, name='api-register'),# User registration endpoint
    path('logout/', views.logout, name='api-logout'),# User logout endpoint
    
    
    #path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    #path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
] 