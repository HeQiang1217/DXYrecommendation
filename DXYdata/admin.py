from django.contrib import admin
from import_export import resources
from DXYdata.models import ProvinceData,CityData,DataAfterPca
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class ProvinceDataResource(resources.ModelResource):

    class Meta:
        model = ProvinceData
        export_order = ('updateTime','provinceName','province_confirmedCount','province_suspectedCount','province_curedCount',
                        'province_deadCount','province_increasedConfirmedCount','province_increasedCuredCount','province_confirmedProportion',
                        'province_currentCount')

class CityDataResource(resources.ModelResource):

    class Meta:
        model = CityData
        export_order = ('updateTime','cityName','city_confirmedCount','city_suspectedCount','city_curedCount',
                        'city_deadCount','city_increasedConfirmedCount','city_increasedCuredCount','city_confirmedProportion',
                        'city_currentCount')

class DataAfterPcaResource(resources.ModelResource):

    class Meta:
        model = DataAfterPca
        export_order = ('pca_1','pca_2')

@admin.register(ProvinceData)
class ProvinceAdmin(ImportExportModelAdmin):
    list_display = ('id','updateTime','provinceName','province_confirmedCount','province_suspectedCount','province_curedCount',
                        'province_deadCount','province_increasedConfirmedCount','province_increasedCuredCount','province_confirmedProportion'
                        ,'province_currentCount')
    search_fields = ('updateTime','provinceName','province_confirmedCount','province_suspectedCount','province_curedCount',
                        'province_deadCount','province_increasedConfirmedCount','province_increasedCuredCount','province_confirmedProportion'
                        ,'province_currentCount')
    resource_class = ProvinceDataResource

@admin.register(CityData)
class CityAdmin(ImportExportModelAdmin):
    list_display = ('id','updateTime','cityName','city_confirmedCount','city_suspectedCount','city_curedCount',
                        'city_deadCount','city_increasedConfirmedCount','city_increasedCuredCount','city_confirmedProportion',
                        'city_currentCount')
    search_fields = ('updateTime','cityName','city_confirmedCount','city_suspectedCount','city_curedCount',
                        'city_deadCount','city_increasedConfirmedCount','city_increasedCuredCount','city_confirmedProportion',
                        'city_currentCount')
    resource_class = CityDataResource

@admin.register(DataAfterPca)
class DataAfterPcaAdmin(ImportExportModelAdmin):
    list_display = ('id','pca_1','pca_2')
    search_fields = ('pca_1','pca_2')
    resource_class = DataAfterPcaResource