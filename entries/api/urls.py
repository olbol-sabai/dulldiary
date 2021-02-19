
from django.urls import path, include
from .views import EntryDetailAPIView, EntryListAPIView


app_name = 'entries'

urlpatterns = [
    path('<id>/', EntryDetailAPIView.as_view(), name='detail'),
    path('', EntryListAPIView.as_view(), name='list'),
]