from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .models import InfoBlock
from .throttling import UserMinuteThrottle
from .serializers import *

User = get_user_model()


@permission_classes([IsAuthenticated])
class InfoBlockCreateView(APIView):
    throttle_classes = [UserMinuteThrottle]

    def post(self, request):
        infoblock = InfoBlockCreateSerializer(data=request.data)
        if infoblock.is_valid():
            infoblock.save(user=request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class InfoBlockDeleteView(APIView):
    throttle_classes = [UserMinuteThrottle]

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
    throttle_classes = [UserMinuteThrottle]

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
            user_id = int(request.query_params.get('user_id'))
            start_block_id = int(request.query_params.get('start_block_id'))
            count = int(request.query_params.get('count'))
            if count < 0:
                raise ValueError
            User.objects.get(pk=user_id)

            infoblocks = (
                InfoBlock.objects.select_related('user')
                .filter(
                    user__id=user_id,
                    id__gt=start_block_id)
                .order_by('id')[:count]
            )

            serializer = InfoBlockDetailSerializer(infoblocks, many=True)
            return Response(serializer.data)

        except (ValueError, TypeError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAdminUser])
class SwitchBanUserView(APIView):
    def post(self, request, pk):
        try:
            action = request.data['action']
            if action not in ['ban', 'unban']:
                raise ValueError
            target_user = User.objects.get(pk=pk)
            if not (target_user.is_staff or target_user.is_superuser):
                if action == 'ban':
                    target_user.is_active = False
                else:
                    target_user.is_active = True
                target_user.save()
                return Response()
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (KeyError, ValueError):
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
    """
    Смена пароля для авторизированного пользователя
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



