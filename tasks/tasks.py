# tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Task, Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .logging_config import logger

@shared_task
def check_task_deadlines():
    now = timezone.now()
    tasks = Task.objects.filter(deadline__lte=now + timezone.timedelta(days=2), deadline__gt=now)
    channel_layer = get_channel_layer()
    for task in tasks:
        days_left = (task.deadline - now).days
        logger.info(f"Task '{task.title}' is due in {days_left} days.")
        notification = Notification.objects.create(
            user=task.user,
            task=task,
            message=f'Task "{task.title}" is due soon.'
        )
        async_to_sync(channel_layer.group_send)(
            f"user_{task.user.id}",
            {
                'type': 'send_notification',
                'notification': notification.message,
            }
        )
