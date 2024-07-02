from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Category, Task
from .serializers import CategorySerializer, TaskSerializer
from django.utils import timezone
from rest_framework.response import Response

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user).order_by('deadline')
        category = self.request.query_params.get('category')
        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        if category:
            queryset = queryset.filter(category__id=category)
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
    category_id = request.query_params.get('category')

    if not category_id:
        return Response({"error": "Category ID is required"}, status=400)

    tasks = Task.objects.filter(user=user, category_id=category_id, status='TODO')
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