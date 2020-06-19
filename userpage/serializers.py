from rest_framework import serializers
from myauth.models import User
from .models import InfoBlock


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


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
