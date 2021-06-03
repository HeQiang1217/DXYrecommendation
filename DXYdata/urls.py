from django.conf.urls import url
from DXYdata import views

urlpatterns = [
    url(r'^numAna$', views.dxyNumAna),
    url(r'^dyMap$', views.dxyDyMap)
]
