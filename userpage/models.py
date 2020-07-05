from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

User = get_user_model()


class Profile(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_activated = models.BooleanField(default=False)

    def __int__(self):
        return self.id

    def __str__(self):
        return f"<{self.user} - {self.name}>"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class InfoBlock(models.Model):
    title = models.CharField(max_length=65, verbose_name='Название')
    content = models.TextField(max_length=650, verbose_name='Содержание')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'{self.profile} - {self.title}'

    class Meta:
        verbose_name = 'Инфоблок'
        verbose_name_plural = 'Инфоблоки'


class Bracelet(models.Model):
    profile = models.ForeignKey(Profile,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                default=None,
                                related_name='bracelets')

    unique_code = models.CharField(unique=True,
                                   max_length=8,
                                   validators=[MinLengthValidator(8)])

    def __int__(self):
        return self.id

    def __str__(self):
        if self.profile != '' and self.profile is not None:
            return f'Присоединён к {self.profile}, id={self.id}'
        else:
            return f'<Not activated>, id={self.id}'

    class Meta:
        verbose_name = 'Носитель'
        verbose_name_plural = 'Носители'
