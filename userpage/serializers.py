from rest_framework import serializers
from .models import InfoBlock, Bracelet, Profile
from django.db import models


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


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bracelet
        fields = ('is_activated',)


class CreateBraceletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bracelet
        fields = ('unique_code',)


class JoinBraceletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bracelet
        fields = ('unique_code',)


class CheckCodeSerializers(serializers.ModelSerializer):
    unique_code = models.CharField(max_length=8, )

    class Meta:
        model = Bracelet


class ProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'name')


class BraceletForProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bracelet
        fields = ('id', 'unique_code')


class ProfileViewListSerializer(serializers.ModelSerializer):
    bracelets = BraceletForProfileSerializer(read_only=True, many=True)

    class Meta:
        model = Profile
        fields = ('name', 'bracelets', 'is_activated')


class NewProfileNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('name',)
