from django.db import models
from django.contrib import admin

# Create your models here.
class ProvinceData(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    updateTime = models.CharField(max_length=64)
    provinceName = models.CharField(max_length=64)
    province_confirmedCount = models.IntegerField()
    province_suspectedCount = models.IntegerField()
    province_curedCount = models.IntegerField()
    province_deadCount = models.IntegerField()
    province_increasedConfirmedCount = models.IntegerField()
    province_increasedCuredCount = models.IntegerField()
    province_confirmedProportion = models.FloatField()
    province_currentCount = models.IntegerField()

class CityData(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    updateTime = models.CharField(max_length=64)
    cityName = models.CharField(max_length=64)
    city_confirmedCount = models.IntegerField()
    city_suspectedCount = models.IntegerField()
    city_curedCount = models.IntegerField()
    city_deadCount = models.IntegerField()
    city_increasedConfirmedCount = models.IntegerField()
    city_increasedCuredCount = models.IntegerField()
    city_confirmedProportion = models.FloatField()
    city_currentCount = models.IntegerField()

class DataAfterPca(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    pca_1 = models.FloatField()
    pca_2 = models.FloatField()

