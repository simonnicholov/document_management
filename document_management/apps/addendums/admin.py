from django.contrib import admin

from document_management.apps.addendums.models import Addendum, AddendumFile


class AddendumAdmin(admin.ModelAdmin):
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


class AddendumFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'addendum', 'file', 'document_document', 'document_category', 'document_type']
    search_fields = ('id', 'addendum',)

    def document_document(self, obj):
        return obj.addendum.document.get_document_type_display()
    document_document.short_description = 'Document'

    def document_category(self, obj):
        return obj.addendum.document.get_category_display()
    document_category.short_description = 'Category'

    def document_type(self, obj):
        return obj.addendum.document.get_type_display()
    document_type.short_description = 'Type'


admin.site.register(Addendum, AddendumAdmin)
admin.site.register(AddendumFile, AddendumFileAdmin)
