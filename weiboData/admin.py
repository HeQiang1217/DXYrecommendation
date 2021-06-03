from django.contrib import admin
from import_export import resources
from weiboData.models import hmData
from import_export.admin import ImportExportModelAdmin


# Register your models here.
class weiboResource(resources.ModelResource):

    class Meta:
        model = hmData
        export_order = ('username','content','time')

@admin.register(hmData)
class MovieAdmin(ImportExportModelAdmin):
    list_display = (
    'username','content','time')
    search_fields = ('username','content','time')
    resource_class = weiboResource