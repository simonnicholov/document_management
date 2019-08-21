from django.contrib import admin

from document_management.apps.documents.models import Document, DocumentFile, DocumentLogs


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'subject', 'partner', 'group', 'category', 'type']
    search_fields = ('id', 'number', 'subject', )


class DocumentFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'document', 'file', 'document_group', 'document_category', 'document_type']
    search_fields = ('id', 'document',)

    def document_group(self, obj):
        return obj.document.get_group_display()
    document_group.short_description = 'Group'

    def document_category(self, obj):
        return obj.document.get_category_display()
    document_category.short_description = 'Category'

    def document_type(self, obj):
        return obj.document.get_type_display()
    document_type.short_description = 'Type'


class DocumentLogsAdmin(admin.ModelAdmin):
    list_display = ['id', 'document_id', 'document_subject', 'reason', 'action', 'value',
                    'updated_by', 'updated_date']
    search_fields = ('id', 'document',)


admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentFile, DocumentFileAdmin)
admin.site.register(DocumentLogs, DocumentLogsAdmin)
