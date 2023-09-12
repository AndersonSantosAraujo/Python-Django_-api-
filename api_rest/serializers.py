from rest_framework import serializers

from .models import User, UserTasks


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'user_email'


class UserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTasks
        fields = ['user_nickname', 'user_task']
