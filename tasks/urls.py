from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, TaskViewSet, schedule_tasks

router = DefaultRouter()
router.register(r'plans', PlanViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('schedule/', schedule_tasks, name='schedule-tasks'),
]
