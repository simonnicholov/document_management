from django.contrib import admin

from document_management.apps.company_regulations.models import CompanyRegulation, CompanyRegulationFile


class CompanyRegulationAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'subject', 'companyregulation_category', 'companyregulation_type']
    search_fields = ('id', 'number', 'subject',)

    def companyregulation_category(self, obj):
        return obj.document.get_group_display()
    companyregulation_category.short_description = 'Category'

    def companyregulation_type(self, obj):
        return obj.document.get_category_display()
    companyregulation_type.short_description = 'Type'


class CompanyRegulationFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'company_regulation', 'file', 'companyregulation_category',
                    'companyregulation_type']
    search_fields = ('id', 'addendum',)

    def companyregulation_category(self, obj):
        return obj.company_regulation.get_category_display()
    companyregulation_category.short_description = 'Category'

    def companyregulation_type(self, obj):
        return obj.company_regulation.get_type_display()
    companyregulation_type.short_description = 'Type'


admin.site.register(CompanyRegulation, CompanyRegulationAdmin)
admin.site.register(CompanyRegulationFile, CompanyRegulationFileAdmin)
