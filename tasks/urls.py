from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, TaskViewSet, schedule_tasks, task_completion_statistics, progress_reports, productivity_trends

router = DefaultRouter()
router.register(r'plans', PlanViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('schedule/', schedule_tasks, name='schedule-tasks'),
    path('analytics/completion/', task_completion_statistics, name='task-completion-statistics'),
    path('analytics/progress/<str:period>/', progress_reports, name='progress-reports'),
    path('analytics/productivity/', productivity_trends, name='productivity-trends'),
]
