from django.urls import path
from .views import *

urlpatterns = [
    path('', NewsListView.as_view()),
    path('count/', NewsListCountView.as_view()),
    path('last/', NewsListLastView.as_view()),
    path('add/', NewsCreateView.as_view()),
    path('delete/<int:pk>', NewsDeleteView.as_view()),
    path('change/<int:pk>', NewsChangeView.as_view()),
]