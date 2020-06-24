from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator, EmailValidator, ValidationError
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth.models import AbstractUser
from .validators import not_empty


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
    email = models.EmailField(unique=False,
                              max_length=255,
                              validators=[EmailValidator, not_empty])
    REQUIRED_FIELDS = ['email', ]
    USERNAME_FIELD = 'username'

    def get_username(self):
        return self.username

