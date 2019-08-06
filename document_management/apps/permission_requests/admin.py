from django.contrib import admin

from document_management.apps.permission_requests.models import PermissionRequest


class PermissionRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'documents', 'user_request']
    search_fields = ('id', 'documents', 'user_request')


admin.site.register(PermissionRequest, PermissionRequestAdmin)
