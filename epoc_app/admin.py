from django.contrib import admin
from .models import Patient, P_info

from import_export import resources
from import_export.admin import ImportExportModelAdmin

class InfoResource(resources.ModelResource):
    class Meta:
        model = P_info

class InfoAdmin(ImportExportModelAdmin):
    resource_class = InfoResource
    list_filter = ["name", "date"]

admin.site.register(Patient)
admin.site.register(P_info, InfoAdmin)