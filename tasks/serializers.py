from rest_framework import serializers
from .models import Category, Task

from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'task', 'message', 'created_at', 'read']
        read_only_fields = ['user', 'task', 'message', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'user', 'name']
        read_only_fields = ['id', 'user']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'user', 'category', 'title', 'description', 'status', 'priority', 'deadline', 'created_at',
                  'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_deadline(self, value):
        from django.utils import timezone
        if value and value < timezone.now():
            raise serializers.ValidationError("The deadline cannot be in the past.")
        return value
