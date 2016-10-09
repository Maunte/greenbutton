import json
from django.shortcuts import render, redirect
from .forms import *
from greenbuttonrest.client import GreenClient
from greenbuttonrest.helper.parser import Parser


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
        if "parsed_xml" in request.session:
            context["parsed_xml"] = request.session["parsed_xml"]
            del request.session["response"]
            del request.session["parsed_xml"]
        else:
            context["parsed_xml"] = ""

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
            if field in ["published_max", "published_min", "updated_max", "updated_min"]:
                data[field] = datetime_converter(input)
            else:
                data[field] = input
    return data, GreenClient()


def default_params(data):
    return {"published_max": data["published_max"], "published_min": data["published_min"],
            "updated_max": data["updated_max"], "updated_min": data["updated_min"],
            "max_results": data["max_results"], "start_index": data["start_index"], "depth": data["depth"]}


def app_info_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("application_information", **params)
    request.session["response"] = response
    try:
        xml = Parser(response)
        request.session["parsed_xml"] = xml.app_info()
    except ValueError:
        pass
    return redirect("/")


def app_info_by_id_view(request):
    data, gc = data_set(request)
    response = gc.execute("application_information", application_information_id=data["app_info_id"])
    request.session["response"] = response
    try:
        xml = Parser(response)
        request.session["parsed_xml"] = xml.app_info_by_id()
    except ValueError:
        pass
    return redirect("/")


def auth_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("authorization", authorization_id=data["auth_id"], **params)
    request.session["response"] = response
    try:
        xml = Parser(response)
        if data["auth_id"] is None:
            request.session["parsed_xml"] = xml.auth()
        else:
            request.session["parsed_xml"] = xml.auth_id()
    except ValueError:
        pass
    return redirect("/")


def batch_bulk_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("batch_bulk", data["bulk_id"], **params)
    request.session["response"] = response
    try:
        xml = Parser(response)
        request.session["parsed_xml"] = xml.batch()
    except ValueError:
        pass
    return redirect("/")


def batch_sub_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("batch_subscription", data["sub_id"], **params)
    request.session["response"] = response
    try:
        xml = Parser(response)
        request.session["parsed_xml"] = xml.batch()
    except ValueError:
        pass
    return redirect("/")


def batch_retail_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("batch_retail", data["retail_id"], **params)
    request.session["response"] = response
    try:
        xml = Parser(response)
        request.session["parsed_xml"] = xml.batch_retail()
    except ValueError:
        pass
    return redirect("/")


def batch_sub_usage_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("batch_subscription_usage", data["sub_id"], data["usage_id"], **params)
    request.session["response"] = response
    try:
        xml = Parser(response)
        request.session["parsed_xml"] = xml.batch()
    except ValueError:
        pass
    return redirect("/")


def electric_power_quality_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("electric_power_quality_summary", data["sub_id"], data["usage_id"],
                          electric_power_quality_summary_id=data["summary_id"], **params)
    request.session["response"] = response
    try:
        xml = Parser(response)
        if data["summary_id"] is None:
            request.session["parsed_xml"] = xml.batch()
        else:
            request.session["parsed_xml"] = xml.electric_power_quality_summary()
    except ValueError:
        pass
    return redirect("/")


def electric_power_usage_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("electric_power_usage_summary", data["sub_id"], data["usage_id"],
                          electric_power_usage_summary_id=data["summary_id"], **params)
    request.session["response"] = response
    try:
        xml = Parser(response)
        if data["summary_id"] is None:
            request.session["parsed_xml"] = xml.electric_power_usage()
        else:
            request.session["parsed_xml"] = xml.electric_power_usage_summary()
    except ValueError:
        pass
    return redirect("/")


def interval_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("interval_block", interval_block_id=data["interval_id"], **params)
    request.session["response"] = response
    return redirect("/")


def specific_interval_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("interval_block_subscription_meter_usage", data["sub_id"], data["usage_id"], data["meter_id"],
                          interval_block_id=data["summary_id"], **params)
    request.session["response"] = response
    return redirect("/")


def local_time_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("local_time_parameter", local_time_parameter_id=data["local_time_id"], **params)
    request.session["response"] = response
    try:
        xml = Parser(response)
        if data["local_time_id"] is None:
            request.session["parsed_xml"] = xml.local_time()
        else:
            request.session["parsed_xml"] = xml.local_time_id()
    except ValueError:
        pass
    return redirect("/")


def meter_reading_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("meter_reading", meter_reading_id=data["meter_id"], **params)
    request.session["response"] = response
    try:
        xml = Parser(response)
        if data["meter_id"] is None:
            request.session["parsed_xml"] = xml.meter_reading()
        else:
            request.session["parsed_xml"] = xml.meter_reading_id()
    except ValueError:
        pass
    return redirect("/")


def meter_reading_sub_usage_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("meter_reading_subscription_usage", data["sub_id"], data["usage_id"], meter_reading_id=data["meter_id"], **params)
    request.session["response"] = response
    try:
        xml = Parser(response)
        request.session["parsed_xml"] = xml.batch()
    except ValueError:
        pass
    return redirect("/")


def reading_type_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("reading_type", reading_type_id=data["reading_type_id"], **params)
    request.session["response"] = response
    try:
        xml = Parser(response)
        if data["reading_type_id"] is None:
            request.session["parsed_xml"] = xml.reading_type()
        else:
            request.session["parsed_xml"] = xml.reading_type_by_id()
    except ValueError:
        pass
    return redirect("/")


def service_status_view(request):
    gc = GreenClient()
    response = gc.execute("service_status")
    request.session["response"] = response
    try:
        xml = Parser(response)
        request.session["parsed_xml"] = xml.service_status()
    except ValueError:
        pass
    return redirect("/")


def usagepoint_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("usage", usage_point_id=data["usage_id"], **params)
    request.session["response"] = response
    try:
        xml = Parser(response)
        if data["usage_id"] is None:
            request.session["parsed_xml"] = xml.usagepoint()
        else:
            request.session["parsed_xml"] = xml.usagepoint_by_id()
    except ValueError:
        pass
    return redirect("/")


def usagepoint_by_sub_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("usage_by_subscription", data["sub_id"], usage_point_id=data["usage_id"], **params)
    request.session["response"] = response
    try:
        xml = Parser(response)
        if data["usage_id"] is None:
            request.session["parsed_xml"] = xml.usagepoint_sub()
        else:
            request.session["parsed_xml"] = xml.usagepoint_sub_by_id()
    except ValueError:
        pass
    return redirect("/")
