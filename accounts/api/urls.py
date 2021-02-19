
from django.urls import path, include
from .views import (
    RegisterUserAPIView, 
    LoginUserAPIView, 
    CountryListView,
    GoogleAuthAPIView,
    ValidateUserFromEmail,
    CustomTokenRefreshView,
    ValidateUserFromResentEmail
    )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)



app_name = 'auth'

urlpatterns = [
    path('login/', LoginUserAPIView.as_view(), name='login'),
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('verify/', TokenVerifyView.as_view(), name='verify'),
    path('confirm-password/', ValidateUserFromEmail.as_view(), name='validate'),
    path('new-confirm-password/', ValidateUserFromResentEmail.as_view(), name='resent_validate'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='refresh'),
    path('token/', TokenObtainPairView.as_view()),
    path('google_auth/', GoogleAuthAPIView.as_view(), name='google_auth'),
    path('country_list/', CountryListView.as_view(), name='country_list'),
]