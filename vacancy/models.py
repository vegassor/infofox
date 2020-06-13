from django.db import models


class Vacancy(models.Model):
    name = models.CharField(max_length=60, verbose_name='Должность')
    description = models.TextField(max_length=150, verbose_name='Описание')
    content = models.TextField(max_length=600, verbose_name='Требования')

    def __str__(self):
        return '- '+self.name

    class Meta:
        verbose_name_plural = 'Вакансии'
        verbose_name = 'Вакансия'
