from django.urls import path
from .views import *


urlpatterns = [
    path('', ViewProfile.as_view()),
    path('add/', CreateProfile.as_view()),
    path('profile/<int:pk>', InfoBlockFromProfileListView.as_view()),
    path('profile/<int:profile_pk>/add/', InfoBlockCreateView.as_view()),
    path('profile/<int:profile_pk>/delete/<int:block_pk>', InfoBlockDeleteView.as_view()),
    path('profile/<int:profile_pk>/change/<int:block_pk>', InfoBlockChangeView.as_view()),
    path('profile/<int:pk>/bracelets', BraceletFromProfile.as_view()),
    path('profile/<int:pk>/disconnect/', DisconnectBracelet.as_view()),
    path('bracelet/add/', createhandler.as_view()),
    path('bracelet/add/many/', CreateManyHandlers.as_view()),
    path('bracelet/delete/<int:pk>', deleteHandler.as_view()),
    path('bracelet/<int:pk>', AccountDefinition.as_view()),
    path('bracelet/registration/<int:pk>', JoinHandler.as_view()),
]
