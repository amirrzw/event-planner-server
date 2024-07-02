from celery import shared_task
from django.utils import timezone
from .models import Task, Notification

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@shared_task
def check_task_deadlines():
    now = timezone.now()
    tasks = Task.objects.filter(deadline__lte=now + timezone.timedelta(hours=1), deadline__gt=now)
    channel_layer = get_channel_layer()
    for task in tasks:
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
