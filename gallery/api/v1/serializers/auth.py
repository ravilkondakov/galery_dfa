from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuthSerializer(serializers.Serializer):
    phone = PhoneNumberField()
    password = serializers.CharField()
