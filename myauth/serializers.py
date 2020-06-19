from django import forms
from django.core.exceptions import ValidationError
from djoser.serializers import UserCreateSerializer, UserSerializer
from .models import *


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password')


def validate_purpose(value):
    if value not in {'question', 'offer', 'jobResponse', 'comment', 'claim'}:
        raise ValidationError(
            "the value should be one of: 'question', 'offer', 'jobResponse', 'comment', 'claim'"
        )


class EmailCommentForm(forms.Form):
    address = forms.EmailField(required=True)
    content = forms.CharField(required=True)
    purpose = forms.CharField(required=True, validators=[validate_purpose])
