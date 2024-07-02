from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, TaskViewSet, schedule_tasks

router = DefaultRouter()
router.register(r'plans', PlanViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('schedule/', schedule_tasks, name='schedule-tasks'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/read/', MarkNotificationAsReadView.as_view(), name='notification-mark-read'),

]
