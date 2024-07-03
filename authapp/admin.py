from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'password')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            # Create a new tuple instead of modifying the existing one
            fieldsets = (
                fieldsets[0],
                (fieldsets[1][0], {'fields': ('password',) + fieldsets[1][1]['fields']}),
                *fieldsets[2:]
            )
        return fieldsets


admin.site.unregister(User)
admin.site.register(User, UserAdmin)