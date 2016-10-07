from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^app-info/', views.app_info_view, name="app-info"),
    url(r'^app-info-id/', views.app_info_by_id_view, name="app-info-id"),
    url(r'^auth/', views.auth_view, name="auth"),
    url(r'^batch-bulk/', views.batch_bulk_view, name="batch-bulk"),
    url(r'^batch-sub/', views.batch_sub_view, name="batch-sub"),
    url(r'^batch-retail/', views.batch_retail_view, name="batch-retail"),
    url(r'^batch-sub-usage/', views.batch_sub_usage_view, name="batch-sub-usage"),
    url(r'^admin/', admin.site.urls),
]
