from django.contrib import admin

from document_management.apps.permission_requests.models import PermissionRequest


class PermissionRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'document', 'user']
    search_fields = ('id', 'document', 'user')


admin.site.register(PermissionRequest, PermissionRequestAdmin)
