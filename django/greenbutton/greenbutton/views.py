from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ParamForm, AppInfobyIdForm
from greenbuttonrest.client import GreenClient


def index(request):
    # Define forms to render
    forms = {
        "app_info": ParamForm,
        "app_info_by_id": AppInfobyIdForm,
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
    
    return redirect("/", response=response)
