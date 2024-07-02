from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import Plan, Task
from datetime import datetime
from django.utils import timezone

class TaskModelTest(TestCase):
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

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'This is a test task')
        self.assertEqual(self.task.status, 'TODO')
        self.assertEqual(self.task.priority, 'HIGH')
        self.assertEqual(str(self.task.deadline), '2024-12-31 23:59:59+00:00')
        self.assertEqual(self.task.user.username, 'testuser')
        self.assertEqual(self.task.plan.title, 'University Plan')
