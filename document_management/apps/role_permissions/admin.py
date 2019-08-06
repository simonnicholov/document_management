from django.contrib import admin

from document_management.apps.role_permissions.models import Role, Permission, RolePermission


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('id', 'name',)


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('id', 'name',)


class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'role', 'permission']
    search_fields = ('id', 'role_id', 'role_name', 'permission_id', 'permission_name')


admin.site.register(Role, RoleAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(RolePermission, RolePermissionAdmin)
