from django.contrib import admin

from document_management.apps.official_records.models import OfficialRecord, OfficialRecordFile


class OfficialRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'subject', 'document_group', 'document_category', 'document_type']
    search_fields = ('id', 'number', 'subject',)

    def document_group(self, obj):
        return obj.document.get_group_display()
    document_group.short_description = 'Group'

    def document_category(self, obj):
        return obj.document.get_category_display()
    document_category.short_description = 'Category'

    def document_type(self, obj):
        return obj.document.get_type_display()
    document_type.short_description = 'Type'


class OfficialRecordFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'official_record', 'file', 'document_group', 'document_category', 'document_type']
    search_fields = ('id', 'official_record',)

    def document_group(self, obj):
        return obj.addendum.document.get_group_display()
    document_group.short_description = 'Group'

    def document_category(self, obj):
        return obj.addendum.document.get_category_display()
    document_category.short_description = 'Category'

    def document_type(self, obj):
        return obj.addendum.document.get_type_display()
    document_type.short_description = 'Type'


admin.site.register(OfficialRecord, OfficialRecordAdmin)
admin.site.register(OfficialRecordFile, OfficialRecordFileAdmin)
