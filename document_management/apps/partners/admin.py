from django.contrib import admin

from document_management.apps.partners.models import Partner


class PartnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ('id', 'name',)


admin.site.register(Partner, PartnerAdmin)
