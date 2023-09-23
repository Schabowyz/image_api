from django.contrib.auth.models import User
from rest_framework import serializers

from .models import ImageContainer


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ["id", "username", "password"]


class ImageContainerSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ImageContainer
        fields = ["id", "images_urls"]