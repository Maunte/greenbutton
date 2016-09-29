from flask import Flask, render_template, request

from GreenButtonRest.clients import GreenButtonClient as gbc
from GreenButtonRest.parser import ParseXml

app2 = Flask(__name__)


def fill_params(data, *exclude):
    params = {}
    for key, value in data.items():
        if key not in exclude and value != "":
            params[key] = value
    return params


class gbcc(object):
    def __init__(self, access_token):
        self.access_token = access_token


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

    call = gbcc(access_token=data["access_token"])
    paths, params = [], {}
    if "app_info_submit" in request.form:
        response = call.execute(endpoint="ApplicationInformation", published_max=data["published-max"],
                                published_min=data["published-min"], updated_max=data["updated-max"],
                                updated_min=data["updated-min"], max_results=data["max-results"],
                                start_index=data["start-index"], depth=data["depth"])
    elif "app_info_id_submit" in data:
        response = call.execute(endpoint="ApplicationInformation", id=data["app_info_id"],
                                published_max=data["published-max"],
                                published_min=data["published-min"], updated_max=data["updated-max"],
                                updated_min=data["updated-min"], max_results=data["max-results"],
                                start_index=data["start-index"], depth=data["depth"])
    elif "auth_submit" in data:
        response = call.execute(endpoint="Authorization", id=data["auth_id"], published_max=data["published-max"],
                                published_min=data["published-min"], updated_max=data["updated-max"],
                                updated_min=data["updated-min"], max_results=data["max-results"],
                                start_index=data["start-index"], depth=data["depth"])
    elif "bulk_submit" in data:
        if "bulk_id" in data:
            response = call.execute(endpoint="Batch/Bulk", bulk_id=data["bulk_id"], published_max=data["published-max"],
                                    published_min=data["published-min"], updated_max=data["updated-max"],
                                    updated_min=data["updated-min"], max_results=data["max-results"],
                                    start_index=data["start-index"], depth=data["depth"])
        elif "ub_id" in data:
            response = call.execute(endpoint="Batch/Subscription", subscription_id=data["sub_id"],
                                    published_max=data["published-max"], published_min=data["published-min"],
                                    updated_max=data["updated-max"], updated_min=data["updated-min"],
                                    max_results=data["max-results"], start_index=data["start-index"],
                                    depth=data["depth"])
        elif "customer_id" in data:
            response = call.execute(endpoint="Batch/RetailCustomer", retail_customer_id=data["customer_id"],
                                    published_max=data["published-max"], published_min=data["published-min"],
                                    updated_max=data["updated-max"], updated_min=data["updated-min"],
                                    max_results=data["max-results"], start_index=data["start-index"],
                                    depth=data["depth"])
        elif "usage_id" in data and "sub_id" in data:
            response = call.execute(endpoint="Batch/Subscription/UsagePoint", subscription_id=data["sub_id"],
                                    usage_id=data["usage_id"], published_max=data["published-max"],
                                    published_min=data["published-min"], updated_max=data["updated-max"],
                                    updated_min=data["updated-min"], max_results=data["max-results"],
                                    start_index=data["start-index"], depth=data["depth"])
    elif "epower_submit" in data:
        if data["epower_radio"] == "quality":
            if data["summary_id"] == "":
                response = call.execute(endpoint="ElectricPowerQualitySummary", subscription_id=data["sub_id"],
                                        usagepoint_id=data["usage_id"], published_max=data["published-max"],
                                        published_min=data["published-min"], updated_max=data["updated-max"],
                                        updated_min=data["updated-min"], max_results=data["max-results"],
                                        start_index=data["start-index"], depth=data["depth"])
            else:
                response = call.execute(endpoint="ElectricPowerQualitySummarybyId", id=data["summary_id"],
                                        subscription_id=data["sub_id"], usagepoint_id=data["usage_id"],
                                        published_max=data["published-max"], published_min=data["published-min"],
                                        updated_max=data["updated-max"], updated_min=data["updated-min"],
                                        max_results=data["max-results"], start_index=data["start-index"],
                                        depth=data["depth"])
        else:
            if data["summary"] == "":
                response = call.execute(endpoint="ElectricPowerUsageSummary", subscription_id=data["sub_id"],
                                        usagepoint_id=data["usage_id"], published_max=data["published-max"],
                                        published_min=data["published-min"], updated_max=data["updated-max"],
                                        updated_min=data["updated-min"], max_results=data["max-results"],
                                        start_index=data["start-index"], depth=data["depth"])
            else:
                response = call.execute(endpoint="ElectricPowerUsageSummarybyId", id=data["summary_id"],
                                        subscription_id=data["sub_id"], usagepoint_id=data["usage_id"],
                                        published_max=data["published-max"], published_min=data["published-min"],
                                        updated_max=data["updated-max"], updated_min=data["updated-min"],
                                        max_results=data["max-results"], start_index=data["start-index"],
                                        depth=data["depth"])
    elif "interval_submit" in data:
        if "sub_id" in data:
            if "interval_id" in data:
                response = call.execute(endpoint="Subscription/IntervalBlockbyId", id=data["interval_id"],
                                        meter_id=data["meter_id"], subscription_id=data["sub_id"],
                                        usagepoint_id=data["usage_id"], published_max=data["published-max"],
                                        published_min=data["published-min"], updated_max=data["updated-max"],
                                        updated_min=data["updated-min"], max_results=data["max-results"],
                                        start_index=data["start-index"], depth=data["depth"])
            else:
                response = call.execute(endpoint="Subscription/IntervalBlock", meter_id=data["meter_id"],
                                        subscription_id=data["sub_id"], usagepoint_id=data["usage_id"],
                                        published_max=data["published-max"], published_min=data["published-min"],
                                        updated_max=data["updated-max"], updated_min=data["updated-min"],
                                        max_results=data["max-results"], start_index=data["start-index"],
                                        depth=data["depth"])
        else:
            response = call.execute(endpoint="IntervalBlock", id=data["interval_id"],
                                    published_max=data["published-max"], published_min=data["published-min"],
                                    updated_max=data["updated-max"], updated_min=data["updated-min"],
                                    max_results=data["max-results"], start_index=data["start-index"],
                                    depth=data["depth"])
    elif "local_time_submit" in data:
        response = call.execute(endpoint="LocalTimeParameters", id=data["local_time_id"],
                                published_max=data["published-max"], published_min=data["published-min"],
                                updated_max=data["updated-max"], updated_min=data["updated-min"],
                                max_results=data["max-results"], start_index=data["start-index"], depth=data["depth"])
    elif "meter_submit" in data:
        if "sub_id" in data:
            if "meter_id" in data:
                response = call.execute(endpoint="Subscription/MeterReadingId", meter_id=data["meter_id"],
                                        subscription_id=data["sub_id"], usage_id=data["usage_id"],
                                        published_max=data["published-max"], published_min=data["published-min"],
                                        updated_max=data["updated-max"], updated_min=data["updated-min"],
                                        max_results=data["max-results"], start_index=data["start-index"],
                                        depth=data["depth"])
            else:
                response = call.execute(endpoint="Subscription/MeterReading", subscription_id=data["sub_id"],
                                        usage_id=data["usage_id"], published_max=data["published-max"],
                                        published_min=data["published-min"], updated_max=data["updated-max"],
                                        updated_min=data["updated-min"], max_results=data["max-results"],
                                        start_index=data["start-index"], depth=data["depth"])
        else:
            response = call.execute(endpoint="MeterReading", id=data["meter_id"], published_max=data["published-max"],
                                    published_min=data["published-min"], updated_max=data["updated-max"],
                                    updated_min=data["updated-min"], max_results=data["max-results"],
                                    start_index=data["start-index"], depth=data["depth"])
    elif "reading_type_submit" in data:
        response = call.execute(endpoint="ReadingType", id=data["reading_type_id"],
                                published_max=data["published-max"],
                                published_min=data["published-min"], updated_max=data["updated-max"],
                                updated_min=data["updated-min"], max_results=data["max-results"],
                                start_index=data["start-index"], depth=data["depth"])
    elif "server_status_submit" in data:
        response = call.execute(endpoint="ReadServiceStatus")
    elif "usagepoint_submit" in data:
        if "sub_id" in data:
            if "usagep_id" in data:
                response = call.execute(endpoint="Subscription/UsagePointbyId", subscription_id=data["sub_id"],
                                        usage_id=data["usage_id"], published_max=data["published-max"],
                                        published_min=data["published-min"], updated_max=data["updated-max"],
                                        updated_min=data["updated-min"], max_results=data["max-results"],
                                        start_index=data["start-index"], depth=data["depth"])
            else:
                response = call.execute(endpoint="Subscription/UsagePoint", subscription_id=data["sub_id"],
                                        published_max=data["published-max"], published_min=data["published-min"],
                                        updated_max=data["updated-max"], updated_min=data["updated-min"],
                                        max_results=data["max-results"], start_index=data["start-index"],
                                        depth=data["depth"])
        else:
            response = call.execute(endpoint="UsagePoint", id=data["usage_id"], published_max=data["published-max"],
                                    published_min=data["published-min"], updated_max=data["updated-max"],
                                    updated_min=data["updated-min"], max_results=data["max-results"],
                                    start_index=data["start-index"], depth=data["depth"])

    try:
        return render_template("index2.html", response=response)
    except:
        return render_template("index2.html")


if __name__ == "__main__":
    app2.run(debug=True)
