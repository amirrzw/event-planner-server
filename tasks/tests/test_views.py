from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from tasks.models import Category, Task

class TaskViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.category = Category.objects.create(user=self.user, name='University')
        self.task_high = Task.objects.create(
            user=self.user,
            category=self.category,
            title='High Priority Task',
            description='This is a high priority task',
            status='TODO',
            priority='HIGH',
            deadline='2024-12-31 23:59:59'
        )
        self.task_low = Task.objects.create(
            user=self.user,
            category=self.category,
            title='Low Priority Task',
            description='This is a low priority task',
            status='TODO',
            priority='LOW',
            deadline='2024-12-31 23:59:59'
        )

    def test_create_task(self):
        url = reverse('task-list')
        data = {
            'category': self.category.id,
            'title': 'New Task',
            'description': 'This is a new task',
            'status': 'TODO',
            'priority': 'MEDIUM',
            'deadline': '2024-12-31 23:59:59'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)

    def test_get_tasks(self):
        url = reverse('task-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_tasks_by_category(self):
        url = f"{reverse('task-list')}?category={self.category.id}"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_tasks_by_status(self):
        url = f"{reverse('task-list')}?status=TODO"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_tasks_by_priority(self):
        url = f"{reverse('task-list')}?priority=HIGH"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'High Priority Task')

    def test_update_task(self):
        url = reverse('task-detail', args=[self.task_high.id])
        data = {
            'category': self.category.id,
            'title': 'Updated Task',
            'description': 'This is an updated task',
            'status': 'IN_PROGRESS',
            'priority': 'LOW',
            'deadline': '2024-12-31 23:59:59'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task_high.refresh_from_db()
        self.assertEqual(self.task_high.title, 'Updated Task')
        self.assertEqual(self.task_high.description, 'This is an updated task')
        self.assertEqual(self.task_high.status, 'IN_PROGRESS')
        self.assertEqual(self.task_high.priority, 'LOW')

    def test_delete_task(self):
        url = reverse('task-detail', args=[self.task_high.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)
