from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'priority', 'deadline', 'created_at', 'updated_at')
    list_filter = ('category', 'priority', 'deadline')
    search_fields = ('title', 'description')
