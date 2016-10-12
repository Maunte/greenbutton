import json, csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from greenbuttonrest.client import GreenClient
from greenbuttonrest.helper.parser import Parser, CsvWriter


def index(request, **kwargs):
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
        try:
            return kwargs["csv"]
        except KeyError:
            pass

        if request.session["response"] is not None:
            xml = Parser(request.session["response"])
            context["json"] = xml.parser()
            request.session["json"] = context["json"]
        else:
            context["response"] = "Failed"
            context["json"] = ""

        context["response"] = request.session["response"]
    else:
        pass
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


def create_csv(jsonfile):
    writer = CsvWriter(jsonfile)
    writer.writecsv()


def download_csv_view(request):
    create_csv(request.session["json"])

    csvresponse = HttpResponse(content_type="text/csv")
    csvresponse['Content-Disposition'] = 'attachment; filename="greenbutton.csv"'

    readfile = open("greenbutton/csv/output.csv", "r")
    writer = csv.writer(csvresponse)

    for line in readfile:
        writer.writerow([line])

    return csvresponse


def app_info_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("application_information", **params)
    request.session["response"] = response
    return redirect("/")


def app_info_by_id_view(request):
    data, gc = data_set(request)
    response = gc.execute("application_information", application_information_id=data["app_info_id"])
    request.session["response"] = response
    return redirect("/")


def auth_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("authorization", authorization_id=data["auth_id"], **params)
    request.session["response"] = response
    return redirect("/")


def batch_bulk_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("batch_bulk", data["bulk_id"], **params)
    request.session["response"] = response
    return redirect("/")


def batch_sub_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("batch_subscription", data["sub_id"], **params)
    request.session["response"] = response
    return redirect("/")


def batch_retail_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("batch_retail", data["retail_id"], **params)
    request.session["response"] = response
    return redirect("/")


def batch_sub_usage_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("batch_subscription_usage", data["sub_id"], data["usage_id"], **params)
    request.session["response"] = response
    return redirect("/")


def electric_power_quality_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("electric_power_quality_summary", data["sub_id"], data["usage_id"],
                          electric_power_quality_summary_id=data["summary_id"], **params)
    request.session["response"] = response
    return redirect("/")


def electric_power_usage_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("electric_power_usage_summary", data["sub_id"], data["usage_id"],
                          electric_power_usage_summary_id=data["summary_id"], **params)
    request.session["response"] = response
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
                          interval_block_id=data["interval_id"], **params)
    request.session["response"] = response
    return redirect("/")


def local_time_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("local_time_parameter", local_time_parameter_id=data["local_time_id"], **params)
    request.session["response"] = response
    return redirect("/")


def meter_reading_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("meter_reading", meter_reading_id=data["meter_id"], **params)
    request.session["response"] = response
    return redirect("/")


def meter_reading_sub_usage_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("meter_reading_subscription_usage", data["sub_id"], data["usage_id"], meter_reading_id=data["meter_id"], **params)
    request.session["response"] = response
    return redirect("/")


def reading_type_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("reading_type", reading_type_id=data["reading_type_id"], **params)
    request.session["response"] = response
    return redirect("/")


def service_status_view(request):
    gc = GreenClient()
    response = gc.execute("service_status")
    request.session["response"] = response
    return redirect("/")


def usagepoint_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("usage", usage_point_id=data["usage_id"], **params)
    request.session["response"] = response
    return redirect("/")


def usagepoint_by_sub_view(request):
    data, gc = data_set(request)
    params = default_params(data)
    response = gc.execute("usage_by_subscription", data["sub_id"], usage_point_id=data["usage_id"], **params)
    request.session["response"] = response
    return redirect("/")
