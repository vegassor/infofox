from django.urls import path
from .views import *

urlpatterns = [
    path('', VacancyListView.as_view()),
    path('<int:pk>/', VacancyDetailView.as_view()),
    path('add/', VacancyCreateView.as_view()),
    path('delete/<int:pk>', VacancyDeleteView.as_view()),
    path('change/<int:pk>', VacancyUpdateView.as_view()),
]
