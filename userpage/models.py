from django.db import models
from myauth.models import User


class InfoBlock(models.Model):
    title = models.CharField(max_length=65, verbose_name='Название')
    content = models.TextField(max_length=650, verbose_name='Содержание')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Инфоблок'
        verbose_name_plural = 'Инфоблоки'
