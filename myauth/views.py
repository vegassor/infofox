from smtplib import SMTPException
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.response import Response

from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created
from django_rest_passwordreset.models import ResetPasswordToken

from .throttling import EmailMinuteThrottle, ServiceUnavailable
from .serializers import EmailCommentForm, EmailSerializer
from .models import User


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def is_admin(request, *args, **kwargs):
    return Response(data={"is_admin": request.user.is_staff}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_superuser(request, *args, **kwargs):
    return Response(data={"is_superuser": request.user.is_superuser}, status=status.HTTP_200_OK)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format('http://coolstorybob.herokuapp.com/password_reset', reset_password_token.key)
    }

    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)
    try:
        msg = EmailMultiAlternatives(
            # title:
            "Восстановление пароля для {title}".format(title="InfoFox"),
            # message:
            email_plaintext_message,
            # from:
            settings.EMAIL_HOST_USER,
            # to:
            [reset_password_token.user.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()
    except (SMTPException, OSError) as e:
        raise ServiceUnavailable(detail=str(e))


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
        except (SMTPException, OSError) as e:
            print(e)
            response_data['email_sent'] = False
            response_data['errors'] = str(e)
            return Response(data=response_data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    else:
        form.errors['email_sent'] = False
        return Response(data=form.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(data=response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_email(request):
    email = EmailSerializer(data=request.data)
    
    if email.is_valid():
        try:
            User.objects.get(email=email.validated_data['email'])
            raise MultipleObjectsReturned
        except ObjectDoesNotExist:
            request.user.email = email.validated_data['email']
            request.user.save()
            return Response(status=status.HTTP_200_OK)
        except MultipleObjectsReturned:
            return Response({"email": "Пользователь с таким email уже существует"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"email": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_in_db(request):
    token = request.data.get('token')
    if token:
        try:
            ResetPasswordToken.objects.get(key=token)
            return Response()
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
