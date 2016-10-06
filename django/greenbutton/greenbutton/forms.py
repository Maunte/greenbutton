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
