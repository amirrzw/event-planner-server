from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import Category, Task
from tasks.serializers import TaskSerializer, CategorySerializer
from django.utils import timezone
from datetime import datetime

class TaskSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(user=self.user, name='University')
        self.task = Task.objects.create(
            user=self.user,
            category=self.category,
            title='Test Task',
            description='This is a test task',
            status='TODO',
            priority='HIGH',
            deadline=datetime(2024, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        )
        self.serializer = TaskSerializer(instance=self.task)

    def test_serializer_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'user', 'category', 'title', 'description', 'status', 'priority', 'deadline', 'created_at', 'updated_at']))

    def test_task_content(self):
        data = self.serializer.data
        self.assertEqual(data['title'], 'Test Task')
        self.assertEqual(data['description'], 'This is a test task')
        self.assertEqual(data['status'], 'TODO')
        self.assertEqual(data['priority'], 'HIGH')
        self.assertEqual(data['deadline'], '2024-12-31T23:59:59Z')  # Updated to match the expected format
        self.assertEqual(data['category'], self.category.id)

class CategorySerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(user=self.user, name='University')
        self.serializer = CategorySerializer(instance=self.category)

    def test_serializer_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'user', 'name']))

    def test_category_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], 'University')
