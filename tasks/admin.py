from django.contrib import admin
from .models import Task, Category

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'priority', 'deadline', 'status', 'created_at', 'updated_at')
    list_filter = ('category', 'priority', 'deadline', 'status')
    search_fields = ('title', 'description', 'user__username', 'category__name')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)
    search_fields = ('name', 'user__username')
