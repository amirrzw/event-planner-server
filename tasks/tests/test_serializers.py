from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import Plan, Task
from tasks.serializers import TaskSerializer, PlanSerializer
from django.utils import timezone
from datetime import datetime

class TaskSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.plan = Plan.objects.create(user=self.user, title='University Plan', description='Plan for university tasks')
        self.task = Task.objects.create(
            user=self.user,
            plan=self.plan,
            title='Test Task',
            description='This is a test task',
            status='TODO',
            priority='HIGH',
            deadline=datetime(2024, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        )
        self.serializer = TaskSerializer(instance=self.task)

    def test_serializer_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'user', 'plan', 'title', 'description', 'status', 'priority', 'deadline', 'created_at', 'updated_at']))

    def test_task_content(self):
        data = self.serializer.data
        self.assertEqual(data['title'], 'Test Task')
        self.assertEqual(data['description'], 'This is a test task')
        self.assertEqual(data['status'], 'TODO')
        self.assertEqual(data['priority'], 'HIGH')
        self.assertEqual(data['deadline'], '2024-12-31T23:59:59Z')
        self.assertEqual(data['plan'], self.plan.id)

class PlanSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.plan = Plan.objects.create(user=self.user, title='University Plan', description='Plan for university tasks')
        self.serializer = PlanSerializer(instance=self.plan)

    def test_serializer_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'user', 'title', 'description']))

    def test_plan_content(self):
        data = self.serializer.data
        self.assertEqual(data['title'], 'University Plan')
        self.assertEqual(data['description'], 'Plan for university tasks')
