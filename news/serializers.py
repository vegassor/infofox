from rest_framework import serializers
from .models import News


class NewsDeleteSerializer(serializers.ModelSerializer):
    """ID новости"""
    class Meta:
        model = News
        fields = ('id',)


class NewsDetailSerializer(serializers.ModelSerializer):
    """Новость со ссылкой на картинку"""
    created_at = serializers.DateTimeField(
        format='%d.%m.%Y',
        required=False,
        read_only=True)

    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'created_at', 'img')


class NewsChangeSerializer(serializers.ModelSerializer):
    """Новость со ссылкой на картинку"""
    created_at = serializers.DateTimeField(
        format='%d.%m.%Y',
        required=False,
        read_only=True)
    img = serializers.ImageField(required=False)

    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'created_at', 'img')