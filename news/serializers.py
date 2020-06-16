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

    # def to_representation(self, instance):
    #     representation = super(NewsListSerializer, self).to_representation(instance)
    #     representation['created_at'] = instance.created_at.strftime('%d.%m.%Y')
    #     return representation

    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'created_at', 'img')
