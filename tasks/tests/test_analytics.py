from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from tasks.models import Category, Task
from datetime import datetime, timedelta
from django.utils import timezone

class AnalyticsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.category = Category.objects.create(user=self.user, name='University')
        self.task1 = Task.objects.create(
            user=self.user,
            category=self.category,
            title='Completed Task 1',
            description='This task is completed',
            status='COMPLETED',
            priority='HIGH',
            deadline=datetime(2024, 12, 31, 23, 59, 59, tzinfo=timezone.utc),
            updated_at=timezone.now() - timedelta(days=1)
        )
        self.task2 = Task.objects.create(
            user=self.user,
            category=self.category,
            title='Pending Task 1',
            description='This task is pending',
            status='TODO',
            priority='MEDIUM',
            deadline=datetime(2024, 11, 30, 23, 59, 59, tzinfo=timezone.utc)
        )

    def test_task_completion_statistics(self):
        url = reverse('task-completion-statistics')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_tasks'], 2)
        self.assertEqual(response.data['completed_tasks'], 1)
        self.assertEqual(response.data['pending_tasks'], 1)

    def test_weekly_progress_reports(self):
        url = reverse('progress-reports', args=['weekly'])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_tasks'], 2)
        self.assertEqual(response.data['completed_tasks'], 1)

    def test_monthly_progress_reports(self):
        url = reverse('progress-reports', args=['monthly'])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_tasks'], 2)
        self.assertEqual(response.data['completed_tasks'], 1)

    def test_productivity_trends(self):
        url = reverse('productivity-trends')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['completed_tasks_per_day']) > 0)
