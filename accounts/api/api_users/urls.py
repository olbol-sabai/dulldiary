
from django.urls import path, include
from .views import (
    UserDetailAPIView, 
    UserListAPIView,
    UploadProfileImageAPIView
    )

app_name = 'users'

urlpatterns = [
    path('', UserListAPIView.as_view(), name='list'),
    path('<username>/', UserDetailAPIView.as_view(), name='detail'),
    path('<username>/upload-profile-image/', UploadProfileImageAPIView.as_view(), name='upload_profile'),
]