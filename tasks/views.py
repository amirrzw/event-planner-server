from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Category, Task
from .serializers import CategorySerializer, TaskSerializer

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
        queryset = Task.objects.filter(user=self.request.user)
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
