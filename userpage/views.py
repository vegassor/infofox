from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from .models import InfoBlock
from myauth.models import User
from .serializers import *


@permission_classes([IsAuthenticated])
class InfoBlockCreateView(APIView):
    def post(self, request):
        infoblock = InfoBlockCreateSerializer(data=request.data)
        if infoblock.is_valid():
            print(infoblock.validated_data)
            infoblock.save(user=request.user)
            print(infoblock.data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class InfoBlockDeleteView(APIView):
    def delete(self, request, pk):
        try:
            infoblock = InfoBlock.objects.get(pk=pk)
            if request.user == infoblock.user:
                infoblock.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAuthenticated])
class InfoBlockChangeView(APIView):
    def put(self, request, pk):
        infoblock_ser = InfoBlockCreateSerializer(data=request.data)
        if infoblock_ser.is_valid():
            try:
                infoblock = InfoBlock.objects.filter(pk=pk)
                if request.user == infoblock[0].user:
                    infoblock.update(**infoblock_ser.data)
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class InfoBlockDetailView(APIView):
    def get(self, request, pk):
        try:
            infoblock = InfoBlock.objects.get(pk=pk)
            serializer = InfoBlockDetailSerializer(infoblock)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([AllowAny])
class InfoBlockListView(APIView):
    def get(self, request):
        try:
            user_id = int(request.data.get('user_id'))
            User.objects.get(pk=user_id)
            infoblocks = InfoBlock.objects.select_related('user').filter(user__id=user_id)
            serializer = InfoBlockDetailSerializer(infoblocks, many=True)
            return Response(serializer.data)
        except (ValueError, TypeError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([AllowAny])
class InfoBlockListCountView(APIView):
    def get(self, request):
        try:
            user_id = int(request.data.get('user_id'))
            start_block_id = int(request.data.get('start_block_id')) + 1
            count = int(request.data.get('count'))
            User.objects.get(pk=user_id)

            infoblocks = (
                InfoBlock.objects.select_related('user')
                .filter(
                    user__id=user_id,
                    id__gte=start_block_id)
                .order_by('id')[:count]
            )

            serializer = InfoBlockDetailSerializer(infoblocks, many=True)
            return Response(serializer.data)

        except (ValueError, TypeError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
