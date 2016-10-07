from django.shortcuts import render, redirect
from .forms import *
from greenbuttonrest.client import GreenClient


def index(request):
    # Define forms to render
    forms = {
        "app_info": ParamForm,
        "app_info_by_id": AppInfobyIdForm,
        "auth": AuthForm,
        "batch_bulk": BatchBulkForm,
        "batch_sub": BatchSubForm,
        "batch_retail": BatchRetailForm,
        "batch_sub_usage": BatchSubUsageForm,
        "electric_power_summary": ElectricPowerSummaryForm,
        "interval": IntervalForm,
        "specific_interval": SpecificIntervalForm,
        "local_time": LocalTimeForm,
        "meter_reading": MeterReadingForm,
        "meter_reading_sub_usage": MeterReadingSubUsageForm,
        "reading_type": ReadingTypeForm,
        "usagepoint": UsagePointForm,
        "usagepoint_by_sub": UsagePointbySubForm,

    }
    context = {}
    if "response" in request.session:
        context["response"] = request.session["response"]
        del request.session["response"]

    return render(request, "greenbutton/index.html", {"forms": forms, "context": context})


def datetime_converter(date):
    datetime = date + "T00:00:00"
    return datetime


def data_set(request):
    data = {}
    for field, input in request.POST.items():
        if input == "":
            data[field] = None
        else:
            if field in ["published-max", "published-min", "updated-max", "updated-min"]:
                data[field] = datetime_converter(input)
            else:
                data[field] = input
    return data, GreenClient()


def app_info_view(request):
    data, gc = data_set(request)
    response = gc.execute("application_information", published_max=data["published_max"],
                          published_min=data["published_min"], updated_max=data["updated_max"],
                          updated_min=data["updated_min"], max_results=data["max_results"],
                          start_index=data["start_index"], depth=data["depth"])
    request.session["response"] = response
    return redirect("/")


def app_info_by_id_view(request):
    data, gc = data_set(request)
    response = gc.execute("application_information", application_information_id=data["app_info_id"])
    request.session["response"] = response
    return redirect("/")


def auth_view(request):
    data, gc = data_set(request)
    response = gc.execute("authorization", authorization_id=data["auth_id"], published_max=data["published_max"],
                          published_min=data["published_min"], updated_max=data["updated_max"],
                          updated_min=data["updated_min"], max_results=data["max_results"],
                          start_index=data["start_index"], depth=data["depth"])
    request.session["response"] = response
    return redirect("/")


def batch_bulk_view(request):
    data, gc = data_set(request)
    response = gc.execute("batch_bulk", data["bulk_id"], published_max=data["published_max"],
                          published_min=data["published_min"], updated_max=data["updated_max"],
                          updated_min=data["updated_min"], max_results=data["max_results"],
                          start_index=data["start_index"], depth=data["depth"])
    request.session["response"] = response
    return redirect("/")


def batch_sub_view(request):
    data, gc = data_set(request)
    response = gc.execute("batch_subscription", data["sub_id"], published_max=data["published_max"],
                          published_min=data["published_min"], updated_max=data["updated_max"],
                          updated_min=data["updated_min"], max_results=data["max_results"],
                          start_index=data["start_index"], depth=data["depth"])
    request.session["response"] = response
    return redirect("/")


def batch_retail_view(request):
    data, gc = data_set(request)
    response = gc.execute("batch_retail", data["retail_id"], published_max=data["published_max"],
                          published_min=data["published_min"], updated_max=data["updated_max"],
                          updated_min=data["updated_min"], max_results=data["max_results"],
                          start_index=data["start_index"], depth=data["depth"])
    request.session["response"] = response
    return redirect("/")


def batch_sub_usage_view(request):
    data, gc = data_set(request)
    response = gc.execute("batch_subscription_usage", data["sub_id"], data["usage_id"],
                          published_max=data["published_max"], published_min=data["published_min"],
                          updated_max=data["updated_max"], updated_min=data["updated_min"],
                          max_results=data["max_results"], start_index=data["start_index"], depth=data["depth"])
    request.session["response"] = response
    return redirect("/")


def electric_power_quality_view(request):
    data, gc = data_set(request)
    response = gc.execute("electric_power_quality_summary", data["sub_id"], data["usage_id"],
                          electric_power_quality_summary_id=data["summary_id"],
                          published_max=data["published_max"], published_min=data["published_min"],
                          updated_max=data["updated_max"], updated_min=data["updated_min"],
                          max_results=data["max_results"], start_index=data["start_index"], depth=data["depth"])
    request.session["response"] = response
    return redirect("/")


def electric_power_usage_view(request):
    data, gc = data_set(request)
    response = gc.execute("electric_power_usage_summary", data["sub_id"], data["usage_id"],
                          electric_power_usage_summary_id=data["summary_id"],
                          published_max=data["published_max"], published_min=data["published_min"],
                          updated_max=data["updated_max"], updated_min=data["updated_min"],
                          max_results=data["max_results"], start_index=data["start_index"], depth=data["depth"])
    request.session["response"] = response
    return redirect("/")


def interval_view(request):
    data, gc = data_set(request)
    response = gc.execute("interval_block", interval_block_id=data["interval_id"], published_max=data["published_max"],
                          published_min=data["published_min"], updated_max=data["updated_max"],
                          updated_min=data["updated_min"], max_results=data["max_results"],
                          start_index=data["start_index"], depth=data["depth"])
    request.session["response"] = response
    return redirect("/")


def specific_interval_view(request):
    data, gc = data_set(request)
    response = gc.execute("interval_block_subscription_meter_usage", data["sub_id"], data["usage_id"], data["meter_id"],
                          interval_block_id=data["summary_id"], published_max=data["published_max"],
                          published_min=data["published_min"], updated_max=data["updated_max"],
                          updated_min=data["updated_min"], max_results=data["max_results"],
                          start_index=data["start_index"], depth=data["depth"])
    request.session["response"] = response
    return redirect("/")


def local_time_view(request):
    data, gc = data_set(request)
    response = gc.execute("local_time_parameter", local_time_parameter_id=data["local_time_id"],
                          published_max=data["published_max"], published_min=data["published_min"],
                          updated_max=data["updated_max"], updated_min=data["updated_min"],
                          max_results=data["max_results"], start_index=data["start_index"], depth=data["depth"])
    request.session["response"] = response
    return redirect("/")


def meter_reading_view(request):
    data, gc = data_set(request)
    response = gc.execute("meter_reading", meter_reading_id=data["meter_id"], published_max=data["published_max"],
                          published_min=data["published_min"], updated_max=data["updated_max"],
                          updated_min=data["updated_min"], max_results=data["max_results"],
                          start_index=data["start_index"], depth=data["depth"])
    request.session["response"] = response
    return redirect("/")


def meter_reading_sub_usage_view(request):
    data, gc = data_set(request)
    response = gc.execute("meter_reading_subscription_usage", data["sub_id"], data["usage_id"],
                          meter_reading_id=data["meter_id"], published_max=data["published_max"],
                          published_min=data["published_min"], updated_max=data["updated_max"],
                          updated_min=data["updated_min"], max_results=data["max_results"],
                          start_index=data["start_index"], depth=data["depth"])
    request.session["response"] = response
    return redirect("/")


def reading_type_view(request):
    data, gc = data_set(request)
    response = gc.execute("reading_type", reading_type_id=data["reading_type_id"], published_max=data["published_max"],
                          published_min=data["published_min"], updated_max=data["updated_max"],
                          updated_min=data["updated_min"], max_results=data["max_results"],
                          start_index=data["start_index"], depth=data["depth"])
    request.session["response"] = response
    return redirect("/")


def service_status_view(request):
    gc = GreenClient()
    response = gc.execute("service_status")
    request.session["response"] = response
    return redirect("/")


def usagepoint_view(request):
    data, gc = data_set(request)
    response = gc.execute("usage", usage_point_id=data["usage_id"], published_max=data["published_max"],
                          published_min=data["published_min"], updated_max=data["updated_max"],
                          updated_min=data["updated_min"], max_results=data["max_results"],
                          start_index=data["start_index"], depth=data["depth"])
    request.session["response"] = response
    return redirect("/")


def usagepoint_by_sub_view(request):
    data, gc = data_set(request)
    response = gc.execute("usage_by_subscription", data["sub_id"], usage_point_id=data["usage_id"],
                          published_max=data["published_max"], published_min=data["published_min"],
                          updated_max=data["updated_max"], updated_min=data["updated_min"],
                          max_results=data["max_results"], start_index=data["start_index"], depth=data["depth"])
    request.session["response"] = response
    return redirect("/")