from flask import Flask, render_template, request

from GreenButtonRest.clientV2 import GreenClient
from GreenButtonRest.parser import ParseXml

app2 = Flask(__name__)


@app2.route("/", methods=['GET', 'POST'])
def main():
    data = {}
    for key, value in request.form.items():
        if "_submit" not in key:
            if value == "":
                data[key] = None
            else:
                data[key] = value
        else:
            pass

    # gc = GreenClient(token=data["access_token"])
    gc = GreenClient()
    paths, params = [], {}
    if "app_info_submit" in request.form:
        response = gc.execute(method="ApplicationInformation", published_max=data["published-max"],
                              published_min=data["published-min"], updated_max=data["updated-max"],
                              updated_min=data["updated-min"], max_results=data["max-results"],
                              start_index=data["start-index"], depth=data["depth"])
    elif "app_info_id_submit" in data:
        response = gc.execute(method="ApplicationInformation", id=data["app_info_id"])
    elif "auth_submit" in data:
        response = gc.execute(method="Authorization", id=data["auth_id"], published_max=data["published-max"],
                              published_min=data["published-min"], updated_max=data["updated-max"],
                              updated_min=data["updated-min"], max_results=data["max-results"],
                              start_index=data["start-index"], depth=data["depth"])
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
    elif "local_time_submit" in data:
        response = gc.execute(method="LocalTimeParameters", id=data["local_time_id"],
                              published_max=data["published-max"], published_min=data["published-min"],
                              updated_max=data["updated-max"], updated_min=data["updated-min"],
                              max_results=data["max-results"], start_index=data["start-index"], depth=data["depth"])
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
    elif "reading_type_submit" in data:
        response = gc.execute(method="ReadingType", id=data["reading_type_id"],
                              published_max=data["published-max"],
                              published_min=data["published-min"], updated_max=data["updated-max"],
                              updated_min=data["updated-min"], max_results=data["max-results"],
                              start_index=data["start-index"], depth=data["depth"])
    elif "server_status_submit" in data:
        response = gc.execute(method="ReadServiceStatus")
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
        return render_template("indexV2.html", response=response)
    except:
        return render_template("indexV2.html")


if __name__ == "__main__":
    app2.run(debug=True)
