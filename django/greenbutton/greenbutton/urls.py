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
    url(r'^electric-power-quality/', views.electric_power_quality_view, name="electric-power-quality"),
    url(r'^electric-power-usage/', views.electric_power_usage_view, name="electric-power-usage"),
    url(r'^interval/', views.interval_view, name="interval"),
    url(r'^specific-interval/', views.specific_interval_view, name="specific-interval"),
    url(r'^local-time/', views.local_time_view, name="local-time"),
    url(r'^meter-reading/', views.meter_reading_view, name="meter-reading"),
    url(r'^meter-reading-sub-usage/', views.meter_reading_sub_usage_view, name="meter-reading-sub-usage"),
    url(r'^reading-type/', views.reading_type_view, name="reading-type"),
    url(r'^service-status/', views.service_status_view, name="service-status"),
    url(r'^usagepoint/', views.usagepoint_view, name="usagepoint"),
    url(r'^usagepoint-by-sub/', views.usagepoint_by_sub_view, name="usagepoint-by-sub"),
    url(r'^admin/', admin.site.urls),
]
