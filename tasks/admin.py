from django.contrib import admin
from .models import Task, Plan

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'plan', 'priority', 'deadline', 'status', 'created_at', 'updated_at')
    list_filter = ('plan', 'priority', 'deadline', 'status')
    search_fields = ('title', 'description', 'user__username', 'plan__title')

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    list_filter = ('user',)
    search_fields = ('title', 'description', 'user__username')
