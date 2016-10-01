from flask import Flask, render_template, request

from GreenButtonRest.client import GreenClient
from GreenButtonRest.parser import ParseXml

app2 = Flask(__name__)


@app2.route("/", methods=['GET', 'POST'])
def main():
    """
    Take form data and put in 'data' dictionary. Ignores submit button name.
    Any form field with a blank value will be given a value of None in 'data'.
    """
    data = {}
    for key, value in request.form.items():
        if value == "":
            data[key] = None
        else:
            data[key] = value

    # gc = GreenClient(token=data["access_token"])
    gc = GreenClient()

    # The GreenClient method that will be called depends on the name of the button used to submit the form.
    # Many submit button names handle several different methods.

    # Application Information Endpoint: No Application Information Id: GET Requests
    if "app_info_submit" in request.form:
        response = gc.execute(method="application_information", published_max=data["published-max"],
                              published_min=data["published-min"], updated_max=data["updated-max"],
                              updated_min=data["updated-min"], max_results=data["max-results"],
                              start_index=data["start-index"], depth=data["depth"])

    # Application Information Endpoint with Id. Note that only the Id is taken as a parameter: GET Requests
    elif "app_info_id_submit" in data:
        response = gc.execute(method="application_information_by_id", id=data["app_info_id"])

    # Authorization Endpoints: GET Requests
    elif "auth_submit" in data:
        response = gc.execute(method="authorization", id=data["auth_id"], published_max=data["published-max"],
                              published_min=data["published-min"], updated_max=data["updated-max"],
                              updated_min=data["updated-min"], max_results=data["max-results"],
                              start_index=data["start-index"], depth=data["depth"])

    # Bulk Transfer Endpoints: GET Requests
    elif "bulk_submit" in data:
        if "bulk_id" in data:
            response = gc.execute(method="Batch/Bulk", bulk_id=data["bulk_id"], published_max=data["published-max"],
                                  published_min=data["published-min"], updated_max=data["updated-max"],
                                  updated_min=data["updated-min"], max_results=data["max-results"],
                                  start_index=data["start-index"], depth=data["depth"])
        elif "sub_id" in data:
            response = gc.execute(method="Batch/Subscription", subscription_id=data["sub_id"],
                                  published_max=data["published-max"], published_min=data["published-min"],
                                  updated_max=data["updated-max"], updated_min=data["updated-min"],
                                  max_results=data["max-results"], start_index=data["start-index"],
                                  depth=data["depth"])
        elif "customer_id" in data:
            response = gc.execute(method="Batch/RetailCustomer", retail_customer_id=data["customer_id"],
                                  published_max=data["published-max"], published_min=data["published-min"],
                                  updated_max=data["updated-max"], updated_min=data["updated-min"],
                                  max_results=data["max-results"], start_index=data["start-index"],
                                  depth=data["depth"])
        elif "usage_id" in data and "sub_id" in data:
            response = gc.execute(method="Batch/Subscription/UsagePoint", subscription_id=data["sub_id"],
                                  usage_id=data["usage_id"], published_max=data["published-max"],
                                  published_min=data["published-min"], updated_max=data["updated-max"],
                                  updated_min=data["updated-min"], max_results=data["max-results"],
                                  start_index=data["start-index"], depth=data["depth"])

    # Electric Power Summaries, both Quality and Usage, Endpoints: Get Requests
    elif "epower_submit" in data:
        if data["epower_radio"] == "quality":
            if data["summary_id"] == "":
                response = gc.execute(method="ElectricPowerQualitySummary", subscription_id=data["sub_id"],
                                      usagepoint_id=data["usage_id"], published_max=data["published-max"],
                                      published_min=data["published-min"], updated_max=data["updated-max"],
                                      updated_min=data["updated-min"], max_results=data["max-results"],
                                      start_index=data["start-index"], depth=data["depth"])
            else:
                response = gc.execute(method="ElectricPowerQualitySummarybyId", id=data["summary_id"],
                                      subscription_id=data["sub_id"], usagepoint_id=data["usage_id"],
                                      published_max=data["published-max"], published_min=data["published-min"],
                                      updated_max=data["updated-max"], updated_min=data["updated-min"],
                                      max_results=data["max-results"], start_index=data["start-index"],
                                      depth=data["depth"])
        else:
            if data["summary"] == "":
                response = gc.execute(method="ElectricPowerUsageSummary", subscription_id=data["sub_id"],
                                      usagepoint_id=data["usage_id"], published_max=data["published-max"],
                                      published_min=data["published-min"], updated_max=data["updated-max"],
                                      updated_min=data["updated-min"], max_results=data["max-results"],
                                      start_index=data["start-index"], depth=data["depth"])
            else:
                response = gc.execute(method="ElectricPowerUsageSummarybyId", id=data["summary_id"],
                                      subscription_id=data["sub_id"], usagepoint_id=data["usage_id"],
                                      published_max=data["published-max"], published_min=data["published-min"],
                                      updated_max=data["updated-max"], updated_min=data["updated-min"],
                                      max_results=data["max-results"], start_index=data["start-index"],
                                      depth=data["depth"])

    # Interval Block Endpoints: GET Requests
    elif "interval_submit" in data:
        if "sub_id" in data:
            if "interval_id" in data:
                response = gc.execute(method="Subscription/IntervalBlockbyId", id=data["interval_id"],
                                      meter_id=data["meter_id"], subscription_id=data["sub_id"],
                                      usagepoint_id=data["usage_id"], published_max=data["published-max"],
                                      published_min=data["published-min"], updated_max=data["updated-max"],
                                      updated_min=data["updated-min"], max_results=data["max-results"],
                                      start_index=data["start-index"], depth=data["depth"])
            else:
                response = gc.execute(method="Subscription/IntervalBlock", meter_id=data["meter_id"],
                                      subscription_id=data["sub_id"], usagepoint_id=data["usage_id"],
                                      published_max=data["published-max"], published_min=data["published-min"],
                                      updated_max=data["updated-max"], updated_min=data["updated-min"],
                                      max_results=data["max-results"], start_index=data["start-index"],
                                      depth=data["depth"])
        else:
            response = gc.execute(method="IntervalBlock", id=data["interval_id"],
                                  published_max=data["published-max"], published_min=data["published-min"],
                                  updated_max=data["updated-max"], updated_min=data["updated-min"],
                                  max_results=data["max-results"], start_index=data["start-index"],
                                  depth=data["depth"])

    # Local Time Parameters Endpoint: GET Requests
    elif "local_time_submit" in data:
        response = gc.execute(method="LocalTimeParameters", id=data["local_time_id"],
                              published_max=data["published-max"], published_min=data["published-min"],
                              updated_max=data["updated-max"], updated_min=data["updated-min"],
                              max_results=data["max-results"], start_index=data["start-index"], depth=data["depth"])

    # Meter Reading Endpoints: GET Requests
    elif "meter_submit" in data:
        if "sub_id" in data:
            if "meter_id" in data:
                response = gc.execute(method="Subscription/MeterReadingId", meter_id=data["meter_id"],
                                      subscription_id=data["sub_id"], usage_id=data["usage_id"],
                                      published_max=data["published-max"], published_min=data["published-min"],
                                      updated_max=data["updated-max"], updated_min=data["updated-min"],
                                      max_results=data["max-results"], start_index=data["start-index"],
                                      depth=data["depth"])
            else:
                response = gc.execute(method="Subscription/MeterReading", subscription_id=data["sub_id"],
                                      usage_id=data["usage_id"], published_max=data["published-max"],
                                      published_min=data["published-min"], updated_max=data["updated-max"],
                                      updated_min=data["updated-min"], max_results=data["max-results"],
                                      start_index=data["start-index"], depth=data["depth"])
        else:
            response = gc.execute(method="MeterReading", id=data["meter_id"], published_max=data["published-max"],
                                  published_min=data["published-min"], updated_max=data["updated-max"],
                                  updated_min=data["updated-min"], max_results=data["max-results"],
                                  start_index=data["start-index"], depth=data["depth"])

    # Reading Type Endpoints: GET Requests
    elif "reading_type_submit" in data:
        response = gc.execute(method="ReadingType", id=data["reading_type_id"],
                              published_max=data["published-max"],
                              published_min=data["published-min"], updated_max=data["updated-max"],
                              updated_min=data["updated-min"], max_results=data["max-results"],
                              start_index=data["start-index"], depth=data["depth"])

    # Service Status Endpoint: GET Request
    elif "server_status_submit" in data:
        response = gc.execute(method="ReadServiceStatus")

    # UsagePoint Endpoints: GET Requests
    elif "usagepoint_submit" in data:
        if "sub_id" in data:
            if "usagep_id" in data:
                response = gc.execute(method="Subscription/UsagePointbyId", subscription_id=data["sub_id"],
                                      usage_id=data["usage_id"], published_max=data["published-max"],
                                      published_min=data["published-min"], updated_max=data["updated-max"],
                                      updated_min=data["updated-min"], max_results=data["max-results"],
                                      start_index=data["start-index"], depth=data["depth"])
            else:
                response = gc.execute(method="Subscription/UsagePoint", subscription_id=data["sub_id"],
                                      published_max=data["published-max"], published_min=data["published-min"],
                                      updated_max=data["updated-max"], updated_min=data["updated-min"],
                                      max_results=data["max-results"], start_index=data["start-index"],
                                      depth=data["depth"])
        else:
            response = gc.execute(method="UsagePoint", id=data["usage_id"], published_max=data["published-max"],
                                  published_min=data["published-min"], updated_max=data["updated-max"],
                                  updated_min=data["updated-min"], max_results=data["max-results"],
                                  start_index=data["start-index"], depth=data["depth"])

    try:
        return render_template("indexV2.html", response=response.text)
    except:
        return render_template("indexV2.html")


if __name__ == "__main__":
    app2.run(debug=True)
