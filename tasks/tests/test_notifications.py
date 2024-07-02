from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from tasks.models import Task, Notification, Plan
from rest_framework_simplejwt.tokens import RefreshToken


class TestNotification(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        self.plan = Plan.objects.create(user=self.user, title="Test Plan", description="Plan description")
        self.task = Task.objects.create(
            user=self.user,
            plan=self.plan,
            title='Test Task',
            description='Task description',
            status='TODO',
            priority='HIGH',
            deadline='2024-07-03T12:00:00Z'
        )
        self.notification = Notification.objects.create(
            user=self.user,
            task=self.task,
            message='Task "Test Task" is due soon.'
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_get_notifications(self):
        url = reverse('notification-list')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['message'], 'Task "Test Task" is due soon.')

    def test_mark_notification_as_read(self):
        url = reverse('notification-mark-read', args=[self.notification.id])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.read)
