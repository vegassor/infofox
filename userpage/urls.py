from django.urls import path
from .views import *


urlpatterns = [
    path('', InfoBlockListView.as_view()),
    path('count/', InfoBlockListCountView.as_view()),
    path('add/', InfoBlockCreateView.as_view()),
    path('delete/<int:pk>', InfoBlockDeleteView.as_view()),
    path('change/<int:pk>', InfoBlockChangeView.as_view()),
    path('<int:pk>', InfoBlockDetailView.as_view()),
]
