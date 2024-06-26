from djoser.serializers import UserSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from .models import FullName
from .models import Game, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    checkpoint = TaskSerializer(many=True)
    author = UserSerializer()

    class Meta:
        model = Game
        fields = ("id", "title", "class_user", "count_checkpoint", "status", "img", "users", "author", "checkpoint")
