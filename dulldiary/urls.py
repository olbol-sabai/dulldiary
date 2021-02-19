
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path('', TemplateView.as_view(template_name='react.html')),
    path('admino/', admin.site.urls),
    path('api/auth/', include('accounts.api.urls', namespace='auth')),
    path('api/users/', include('accounts.api.api_users.urls', namespace='users')),
    path('api/entries/', include('entries.api.urls', namespace='entries')),
    re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name='react.html')),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)