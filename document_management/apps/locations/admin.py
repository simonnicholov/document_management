from django.contrib import admin

from document_management.apps.locations.models import Location


class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']
    search_fields = ('id', 'code', 'name',)


admin.site.register(Location, LocationAdmin)
