from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny

from .models import News
from .serializers import *


@permission_classes([AllowAny])
class NewsListView(APIView):
    """Вывод списка вакансий"""
    def get(self, request):
        vacancies = News.objects.all()
        serializer = NewsDetailSerializer(vacancies, many=True)
        return Response(serializer.data)


@permission_classes([AllowAny])
class NewsListCountView(APIView):
    def get(self, request):
        try:
            start_news_id = int(request.query_params.get('start_news_id'))
            count = int(request.query_params.get('count'))
            if count < 0:
                raise ValueError

            news_query = (
                News.objects
                .filter(id__lt=start_news_id)
                .order_by('-id')[:count]
            )

            serializer = NewsDetailSerializer(news_query, many=True)
            return Response(serializer.data)

        except (ValueError, TypeError):
            return Response(status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class NewsListLastView(APIView):
    def get(self, request):
        try:
            count = int(request.query_params.get('count'))
            if count < 0:
                raise ValueError

            news_query = (
                News.objects
                .order_by('-id')[:count]
            )

            serializer = NewsDetailSerializer(news_query, many=True)
            return Response(serializer.data)

        except (ValueError, TypeError):
            return Response(status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAdminUser])
class NewsCreateView(APIView):
    def post(self, request):
        news = NewsDetailSerializer(data=request.data)
        if news.is_valid():
            print(news.validated_data)
            news.save()
            print(news.data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAdminUser])
class NewsChangeView(APIView):
    def put(self, request, pk):
        news_ser = NewsDetailSerializer(data=request.data)
        if news_ser.is_valid():
            try:
                news = News.objects.get(pk=pk)
                news.title = news_ser.validated_data['title']
                news.content = news_ser.validated_data['content']
                news.img = request.FILES['img']
                news.save()
                return Response(status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAdminUser])
class NewsDeleteView(APIView):
    def delete(self, request, pk):
        try:
            news = News.objects.get(pk=pk)
            news.delete()
            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
