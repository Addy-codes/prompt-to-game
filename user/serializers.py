from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    firebase_uid = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = "__all__"
