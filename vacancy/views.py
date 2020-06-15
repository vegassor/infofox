from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Vacancy
from .serializers import *


class VacancyListView(APIView):
    """Вывод списка вакансий"""
    def get(self, request):
        vacancies = Vacancy.objects.all()
        serializer = VacancyListSerializer(vacancies, many=True)
        return Response(serializer.data)


class VacancyDetailView(APIView):
    """Вывод одной вакансии полностью"""
    def get(self, request, pk):
        try:
            vacancy = Vacancy.objects.get(pk=pk)
            serializer = VacancyDetailSerializer(vacancy)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=404)

@permission_classes([IsAdminUser])
class VacancyCreateView(APIView):
    """Добавление вакансии (админ)"""
    def post(self, request):
        vacancy = VacancyDetailSerializer(data=request.data)
        if vacancy.is_valid():
            vacancy.save()
            return Response(status=201)
        return Response(status=400)


@permission_classes([IsAdminUser])
class VacancyDeleteView(APIView):
    """Удаление вакансии (админ)"""
    def delete(self, request, pk):
        try:
            vacancy = Vacancy.objects.get(pk=pk)
            vacancy.delete()
            return Response(status=200)
        except ObjectDoesNotExist:
            return Response(status=404)


@permission_classes([IsAdminUser])
class VacancyUpdateView(APIView):
    """Изменение вакансии (админ)"""
    def put(self, request, pk):
        vacancy_s = VacancyDetailSerializer(data=request.data)
        if vacancy_s.is_valid():
            try:
                vacancy = Vacancy.objects.filter(pk=pk)
                vacancy.update(**vacancy_s.data)
                return Response(status=200)
            except ObjectDoesNotExist:
                return Response(status=404)
        return Response(status=400)

'''
//my test data//
{
"name": "a",
"description": "b",
"content": "c"
}
'''