from django import forms
from django.forms.widgets import Input


class HTML5DateTimeInput(Input):
    input_type = "date"


class ParamForm(forms.Form):
    published_min = forms.CharField(label="Published Min (optional)", required=False, widget=HTML5DateTimeInput())
    published_max = forms.CharField(label="Published Max (optional)", required=False, widget=HTML5DateTimeInput())
    updated_min = forms.CharField(label="Updated Min (optional)", required=False, widget=HTML5DateTimeInput())
    updated_max = forms.CharField(label="Updated Max (optional)", required=False, widget=HTML5DateTimeInput())
    max_results = forms.IntegerField(label="Max Results (optional)", required=False)
    start_index = forms.IntegerField(label="Start Index (optional)", required=False)
    depth = forms.IntegerField(label="Depth (optional)", required=False)


class AppInfobyIdForm(forms.Form):
    app_info_id = forms.IntegerField(label="Application Information Id (required)")
    field_order = ["app_info_id"]


class AuthForm(ParamForm):
    auth_id = forms.IntegerField(label="Authorization Id", required=False)
    field_order = ["auth_id"]


class BatchBulkForm(ParamForm):
    bulk_id = forms.IntegerField(label="Batch Bulk Id (required)")
    field_order = ["bulk_id"]


class BatchSubForm(ParamForm):
    sub_id = forms.IntegerField(label="Batch Subscription Id (required)")
    field_order = ["sub_id"]


class BatchRetailForm(ParamForm):
    retail_id = forms.IntegerField(label="Batch Retail Customer Id (required)")
    field_order = ["retail_id"]


class BatchSubUsageForm(ParamForm):
    sub_id = forms.IntegerField(label="Batch Subscription Id (required)")
    usage_id = forms.IntegerField(label="Batch UsagePoint Id (required)")
    field_order = ["sub_id", "usage_id"]


class ElectricPowerSummaryForm(ParamForm):
    sub_id = forms.IntegerField(label="Subscription Id (required)")
    usage_id = forms.IntegerField(label="UsagePoint Id (required)")
    summary_id = forms.IntegerField(label="Electric Power Summary Id (optional)", required=False)
    field_order = ["sub_id", "usage_id", "summary_id (required)"]


class IntervalForm(ParamForm):
    interval_id = forms.IntegerField(label="Interval Id (optional)", required=False)
    field_order = ["interval_id"]


class SpecificIntervalForm(ParamForm):
    sub_id = forms.IntegerField(label="Subscription Id (required)")
    usage_id = forms.IntegerField(label="UsagePoint Id (required)")
    meter_id = forms.IntegerField(label="Meter Id (required)")
    interval_id = forms.IntegerField(label="Interval Id (optional)", required=False)
    field_order = ["interval_id", "sub_id", "usage_id", "meter_id"]


class LocalTimeForm(ParamForm):
    local_time_id = forms.IntegerField(label="Local Time Parameter Id (optional)", required=False)
    field_order = ["local_time_id"]


class MeterReadingForm(ParamForm):
    meter_id = forms.IntegerField(label="Meter Reading Id (optional)", required=False)
    field_order = ["meter_id"]


class MeterReadingSubUsageForm(ParamForm):
    sub_id = forms.IntegerField(label="Subscription Id (required)")
    usage_id = forms.IntegerField(label="UsagePoint Id (required)")
    meter_id = forms.IntegerField(label="Meter Id (optional", required=False)
    field_order = ["meter_id", "sub_id", "usage_id"]


class ReadingTypeForm(ParamForm):
    reading_type_id = forms.IntegerField(label="Reading Type Id (optional)", required=False)
    field_order = ["reading_type_id"]


class UsagePointForm(ParamForm):
    usage_id = forms.IntegerField(label="UsagePoint Id (optional)", required=False)
    field_order = ["usage_id"]


class UsagePointbySubForm(ParamForm):
    sub_id = forms.IntegerField(label="Subscription Id (required)")
    usage_id = forms.IntegerField(label="UsagePoint Id (optional)", required=False)
    field_order = ["sub_id", "usage_id"]