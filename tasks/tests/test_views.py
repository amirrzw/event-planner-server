from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from tasks.models import Plan, Task
from datetime import datetime
from django.utils import timezone

class TaskViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.plan = Plan.objects.create(user=self.user, title='University Plan', description='Plan for university tasks')
        self.task1 = Task.objects.create(
            user=self.user,
            plan=self.plan,
            title='First Task',
            description='This is the first task',
            status='TODO',
            priority='HIGH',
            deadline=datetime(2024, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        )
        self.task2 = Task.objects.create(
            user=self.user,
            plan=self.plan,
            title='Second Task',
            description='This is the second task',
            status='TODO',
            priority='MEDIUM',
            deadline=datetime(2024, 11, 30, 23, 59, 59, tzinfo=timezone.utc)
        )
        self.task3 = Task.objects.create(
            user=self.user,
            plan=self.plan,
            title='Third Task',
            description='This is the third task',
            status='TODO',
            priority='LOW',
            deadline=datetime(2024, 10, 31, 23, 59, 59, tzinfo=timezone.utc)
        )

    def test_create_task(self):
        url = reverse('task-list')
        data = {
            'plan': self.plan.id,
            'title': 'New Task',
            'description': 'This is a new task',
            'status': 'TODO',
            'priority': 'MEDIUM',
            'deadline': '2024-12-31 23:59:59'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 4)

    def test_get_tasks(self):
        url = reverse('task-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_tasks_by_plan(self):
        url = f"{reverse('task-list')}?plan={self.plan.id}"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_tasks_by_status(self):
        url = f"{reverse('task-list')}?status=TODO"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_tasks_by_priority(self):
        url = f"{reverse('task-list')}?priority=HIGH"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_tasks_sorted_by_deadline(self):
        url = reverse('task-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        # Check the order of tasks by deadline
        deadlines = [task['deadline'] for task in response.data]
        self.assertEqual(deadlines, [
            '2024-10-31T23:59:59Z',
            '2024-11-30T23:59:59Z',
            '2024-12-31T23:59:59Z'
        ])

    def test_update_task(self):
        url = reverse('task-detail', args=[self.task1.id])
        data = {
            'plan': self.plan.id,
            'title': 'Updated Task',
            'description': 'This is an updated task',
            'status': 'IN_PROGRESS',
            'priority': 'LOW',
            'deadline': '2024-12-31 23:59:59'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Task')
        self.assertEqual(self.task1.description, 'This is an updated task')
        self.assertEqual(self.task1.status, 'IN_PROGRESS')
        self.assertEqual(self.task1.priority, 'LOW')

    def test_delete_task(self):
        url = reverse('task-detail', args=[self.task1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 2)

class TaskSchedulingTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.plan = Plan.objects.create(user=self.user, title='University Plan', description='Plan for university tasks')
        self.task1 = Task.objects.create(
            user=self.user,
            plan=self.plan,
            title='First Task',
            description='This is the first task',
            status='TODO',
            priority='HIGH',
            deadline=datetime(2024, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        )
        self.task2 = Task.objects.create(
            user=self.user,
            plan=self.plan,
            title='Second Task',
            description='This is the second task',
            status='TODO',
            priority='MEDIUM',
            deadline=datetime(2024, 11, 30, 23, 59, 59, tzinfo=timezone.utc)
        )
        self.task3 = Task.objects.create(
            user=self.user,
            plan=self.plan,
            title='Third Task',
            description='This is the third task',
            status='TODO',
            priority='LOW',
            deadline=datetime(2024, 10, 31, 23, 59, 59, tzinfo=timezone.utc)
        )

    def test_schedule_tasks(self):
        url = f"{reverse('schedule-tasks')}?plan={self.plan.id}"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        # Check the order of tasks by the scheduling algorithm
        expected_order = ['First Task', 'Second Task', 'Third Task']
        returned_order = [task['title'] for task in response.data]
        self.assertEqual(returned_order, expected_order)
