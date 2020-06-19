from django.urls import path, include
from. views import *

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('send_email/', send_email),
    path('password_reset/', include('django_rest_passwordreset.urls')),
]
