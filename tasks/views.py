from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import timedelta
from django.db.models import Count

from .models import Plan, Task
from .serializers import PlanSerializer, TaskSerializer


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Plan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user).order_by('deadline')
        plan = self.request.query_params.get('plan')
        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        if plan:
            queryset = queryset.filter(plan__id=plan)
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def schedule_tasks(request):
    user = request.user
    plan_id = request.query_params.get('plan')

    if not plan_id:
        return Response({"error": "Plan ID is required"}, status=400)

    tasks = Task.objects.filter(user=user, plan_id=plan_id, status='TODO')
    current_time = timezone.now()

    def calculate_score(task):
        priority_weight = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}[task.priority]
        time_to_deadline = (task.deadline - current_time).total_seconds()
        if time_to_deadline <= 0:
            return float('inf')  # Overdue tasks get highest priority
        return priority_weight / time_to_deadline

    sorted_tasks = sorted(tasks, key=calculate_score, reverse=True)
    serializer = TaskSerializer(sorted_tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_completion_statistics(request):
    user = request.user
    total_tasks = Task.objects.filter(user=user).count()
    completed_tasks = Task.objects.filter(user=user, status='COMPLETED').count()
    pending_tasks = total_tasks - completed_tasks

    data = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def progress_reports(request, period='weekly'):
    user = request.user
    now = timezone.now()
    if period == 'weekly':
        start_date = now - timedelta(days=7)
    elif period == 'monthly':
        start_date = now - timedelta(days=30)
    else:
        return Response({"error": "Invalid period. Use 'weekly' or 'monthly'."}, status=400)

    tasks = Task.objects.filter(user=user, created_at__gte=start_date)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='COMPLETED').count()

    data = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def productivity_trends(request):
    user = request.user
    now = timezone.now()
    start_date = now - timedelta(days=30)
    completed_tasks_per_day = Task.objects.filter(
        user=user,
        status='COMPLETED',
        updated_at__gte=start_date
    ).extra({'day': 'date( updated_at )'}).values('day').annotate(completed=Count('id')).order_by('day')

    data = {
        'completed_tasks_per_day': list(completed_tasks_per_day),
    }
    return Response(data)