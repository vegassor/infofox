from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from smtplib import SMTPException
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import InfoBlock
from myauth.models import User
from .throttling import EmailMinuteThrottle
from .serializers import *


@permission_classes([IsAuthenticated])
class InfoBlockCreateView(APIView):
    def post(self, request):
        infoblock = InfoBlockCreateSerializer(data=request.data)
        if infoblock.is_valid():
            infoblock.save(user=request.user)
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


@api_view(['POST'])
@throttle_classes([EmailMinuteThrottle])
@permission_classes([AllowAny])
def send_email(request):
    response_data = {}
    purpose_dict = {
        'question': 'Вопрос по продукту',
        'offer': 'Предложение',
        'comment': 'Отзыв',
        'jobResponse': 'Отклик на вакансию',
        'claim': 'Жалоба',
    }
    print(request.headers)
    form = EmailCommentForm(request.POST)
    if form.is_valid():
        try:
            subject = purpose_dict[request.POST.get('purpose')]
            username = request.user.username
            if not request.user.is_authenticated:
                username = 'анонимного пользователя'
            body = request.POST.get('content')
            email = request.POST.get('address')
            body = f'{subject} от {username}:\n{body}\n\nОставленный email: {email}'
            send_mail(subject, body, 'f4ffaa@yandex.ru', ['f4ffaa@yandex.ru'], fail_silently=False)
            response_data['email_sent'] = True
        except SMTPException as e:
            print(e)
            response_data['email_sent'] = False
            response_data['errors'] = str(e)
            return Response(data=response_data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    else:
        form.errors['email_sent'] = False
        return Response(data=form.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(data=response_data, status=status.HTTP_200_OK)
