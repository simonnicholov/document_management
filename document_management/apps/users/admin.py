from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_legal',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'type',)}),
    )

    list_display = ('email', 'name', 'is_superuser', 'is_staff', 'is_legal',)
    list_filter = ('is_staff', 'is_superuser', 'is_legal',  'is_active',)
    search_fields = ('email', 'name',)
    ordering = ('email',)


admin.site.register(User, UserAdmin)
