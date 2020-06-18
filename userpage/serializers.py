from django import forms
from django.core.exceptions import ValidationError
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


class EmailRequestSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


def validate_purpose(value):
    if value not in {'question', 'offer', 'jobResponse', 'comment', 'claim'}:
        raise ValidationError(
            "the value should be one of: 'question', 'offer', 'jobResponse', 'comment', 'claim'"
        )


class EmailCommentForm(forms.Form):
    address = forms.EmailField(required=True)
    content = forms.CharField(required=True)
    purpose = forms.CharField(required=True, validators=[validate_purpose])
