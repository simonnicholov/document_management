from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',)}),
    )

    list_display = ('email', 'name', 'user_role', 'is_superuser', 'is_staff',)
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
    search_fields = ('email', 'name',)
    ordering = ('email',)

    def user_role(self, obj):
        return obj.role.name
    user_role.short_description = 'Role'


admin.site.register(User, UserAdmin)
