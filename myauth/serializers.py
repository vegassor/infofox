from django import forms
from djoser.conf import settings
from rest_framework_recaptcha.fields import ReCaptchaField
from .models import User
from .validators import validate_purpose
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from rest_framework import serializers

# class UserCreateSerializer2(UserCreateSerializer):
#     recaptcha = ReCaptchaField()
#
#     # def is_valid(self, raise_exception=False):
#     #     valid = super().is_valid(raise_exception=raise_exception)
#     #     return valid
#
#     class Meta(UserCreateSerializer.Meta):
#         model = User
#         fields = ('id', 'email', 'username', 'password', 'recaptcha')
#
#     def create(self, validated_data):
#         print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
#         return super().create(validated_data)


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    recaptcha = ReCaptchaField()
    default_error_messages = {
        "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            User._meta.pk.name,
            "password",
            "recaptcha"
        )

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user


class EmailCommentForm(forms.Form):
    address = forms.EmailField(required=True)
    content = forms.CharField(required=True)
    purpose = forms.CharField(required=True, validators=[validate_purpose])
