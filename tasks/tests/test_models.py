from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import Category, Task

class TaskModelTest(TestCase):
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
            deadline='2024-12-31 23:59:59'
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'This is a test task')
        self.assertEqual(self.task.status, 'TODO')
        self.assertEqual(self.task.priority, 'HIGH')
        self.assertEqual(str(self.task.deadline), '2024-12-31 23:59:59')
        self.assertEqual(self.task.user.username, 'testuser')
        self.assertEqual(self.task.category.name, 'University')
