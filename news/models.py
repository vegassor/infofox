from django.db import models


class News(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=150, verbose_name='Название')
    content = models.TextField(max_length=3000, verbose_name='Содержание')
    img = models.ImageField(upload_to='%Y_%m_%d', null=False, blank=False)

    def __str__(self):
        return '- '+self.title

    class Meta:
        verbose_name_plural = 'Новости'
        verbose_name = 'Новость'
