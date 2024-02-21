from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import *


class UGGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UGGame
        fields = '__all__'


class imageAssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image_Assets
        fields = '__all__'


class soundAssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sound_Asset
        fields = '__all__'


class RimoraiSerializer(serializers.ModelSerializer):
    image_asset = imageAssetsSerializer(many=True)
    sound_assets = soundAssetsSerializer(many=True)

    class Meta:
        model = Game
        fields = '__all__'
