from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(r'^[a-zA-Z0-9_\-\.]+$',
                                   'Имя пользователя должно состоять из английских букв, цифр и -,_,.'),
                    ASCIIUsernameValidator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    email = models.EmailField(unique=True, max_length=255)
    REQUIRED_FIELDS = ['email', ]
    USERNAME_FIELD = 'username'

    def get_username(self):
        return self.username
