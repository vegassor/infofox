from django.urls import path, include
from. views import *

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/is_admin/', is_admin),
    path('auth/is_superuser/', is_superuser),
    path('send_email/', send_email),
    path('change_email/', change_email),
    path('password_reset/check/', token_in_db),
    path('password_reset/', include('django_rest_passwordreset.urls')),
]
