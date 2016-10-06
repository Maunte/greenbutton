from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^app-info/', views.app_info_view, name="app-info"),
    url(r'^app-info-id/', views.app_info_by_id_view, name="app-info-id"),
    url(r'^admin/', admin.site.urls),
]
