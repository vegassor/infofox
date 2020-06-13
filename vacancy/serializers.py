from rest_framework import serializers
from .models import Vacancy


class VacancyListSerializer(serializers.ModelSerializer):
    """Список вакансий"""
    class Meta:
        model = Vacancy
        fields = ('id', 'name', 'description')


class VacancyDetailSerializer(serializers.ModelSerializer):
    """Одна полная вакансия"""
    class Meta:
        model = Vacancy
        fields = '__all__'
        # exclude = ('id',)