from rest_framework import serializers
from .models import InfoBlock


class InfoBlockDeleteSerializer(serializers.ModelSerializer):
    """ID блока"""
    class Meta:
        model = InfoBlock
        fields = ('id',)


class InfoBlockDetailSerializer(serializers.ModelSerializer):
    """Один инфоблок"""
    class Meta:
        model = InfoBlock
        fields = ('id', 'title', 'content')


class InfoBlockCreateSerializer(serializers.ModelSerializer):
    """Содержание блока"""
    class Meta:
        model = InfoBlock
        fields = ('title', 'content')
