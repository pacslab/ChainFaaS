from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from providers_app.models import Job

# Register your models here.
# admin.site.register(Job)
@admin.register(Job)
class JobAdmin(ImportExportModelAdmin):
    pass