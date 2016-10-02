import json, sys, os

from flask import Flask, render_template, request

sys.path.append(os.path.abspath('.'))
from greenbuttonrest.client import GreenClient
from greenbuttonrest.parser import ParseXml

app = Flask(__name__)


def id_check(data, data_key):
    if data_key in data:
        return data[data_key]
    else:
        return None


@app.route("/", methods=['GET', 'POST'])
def main():
    """
    Take form data and put in 'data' dictionary. Ignores submit button name.
    Any form field with a blank value will be given a value of None in 'data'.
    """
    response = None
    data, context = {}, {}

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
        method = "application_information"
        response = gc.execute(method, published_max=data["published-max"],
                              published_min=data["published-min"], updated_max=data["updated-max"],
                              updated_min=data["updated-min"], max_results=data["max-results"],
                              start_index=data["start-index"], depth=data["depth"])

    # Application Information Endpoint with Id. Note that only the Id is taken as a parameter: GET Requests
    elif "app_info_id_submit" in data:
        method = "application_information"
        response = gc.execute(method, application_information_id=data["app_info_id"])

    # Authorization Endpoints: GET Requests
    elif "auth_submit" in data:
        method = "authorization"
        response = gc.execute(method, authorization_id=data["auth_id"], published_max=data["published-max"],
                              published_min=data["published-min"], updated_max=data["updated-max"],
                              updated_min=data["updated-min"], max_results=data["max-results"],
                              start_index=data["start-index"], depth=data["depth"])

    # Bulk Transfer Endpoints: GET Requests
    elif "bulk_submit" in data:
        if "bulk_id" in data:
            method = "batch_bulk"
            response = gc.execute(method, data["bulk_id"], published_max=data["published-max"],
                                  published_min=data["published-min"], updated_max=data["updated-max"],
                                  updated_min=data["updated-min"], max_results=data["max-results"],
                                  start_index=data["start-index"], depth=data["depth"])
        elif "sub_id" in data:
            method = "batch_subscription"
            response = gc.execute(method, data["sub_id"], published_max=data["published-max"],
                                  published_min=data["published-min"], updated_max=data["updated-max"],
                                  updated_min=data["updated-min"], max_results=data["max-results"],
                                  start_index=data["start-index"], depth=data["depth"])
        elif "customer_id" in data:
            method = "batch_retail"
            response = gc.execute(method, data["customer_id"], published_max=data["published-max"],
                                  published_min=data["published-min"], updated_max=data["updated-max"],
                                  updated_min=data["updated-min"], max_results=data["max-results"],
                                  start_index=data["start-index"], depth=data["depth"])
        elif "usage_id" in data and "sub_id" in data:
            method = "batch_subscription_usage"
            response = gc.execute(method, data["sub_id"], data["usage_id"], published_max=data["published-max"],
                                  published_min=data["published-min"], updated_max=data["updated-max"],
                                  updated_min=data["updated-min"], max_results=data["max-results"],
                                  start_index=data["start-index"], depth=data["depth"])

    # Electric Power Summaries, both Quality and Usage, Endpoints: Get Requests
    elif "epower_submit" in data:
        summary_id = id_check(data, "summary_id")
        if data["epower_radio"] == "quality":
            method = "electric_power_quality_summary"
            response = gc.execute(method, data["sub_id"], data["usage_id"],
                                  electric_power_quality_summary_id=summary_id, published_max=data["published-max"],
                                  published_min=data["published-min"], updated_max=data["updated-max"],
                                  updated_min=data["updated-min"], max_results=data["max-results"],
                                  start_index=data["start-index"], depth=data["depth"])
        else:
            method = "electric_power_usage_summary"
            response = gc.execute(method, data["sub_id"], data["usage_id"],
                                  electric_power_usage_summary_id=summary_id, published_max=data["published-max"],
                                  published_min=data["published-min"], updated_max=data["updated-max"],
                                  updated_min=data["updated-min"], max_results=data["max-results"],
                                  start_index=data["start-index"], depth=data["depth"])

    # Interval Block Endpoints: GET Requests
    elif "interval_submit" in data:
        interval_id = id_check(data, "interval_id")
        if "sub_id" in data:
            method = "interval_block_subscription_meter_usage"
            response = gc.execute(method, data["sub_id"], data["usage_id"], data["meter_id"], id=data["interval_id"],
                                  published_max=data["published-max"], published_min=data["published-min"],
                                  updated_max=data["updated-max"], updated_min=data["updated-min"],
                                  max_results=data["max-results"], start_index=data["start-index"], depth=data["depth"])
        else:
            method = "interval_block"
            response = gc.execute(method, interval_id, published_max=data["published-max"],
                                  published_min=data["published-min"], updated_max=data["updated-max"],
                                  updated_min=data["updated-min"], max_results=data["max-results"],
                                  start_index=data["start-index"], depth=data["depth"])

    # Local Time Parameters Endpoint: GET Requests
    elif "local_time_submit" in data:
        local_time_id = id_check(data, "local_time_id")
        method = "local_time_parameter"
        response = gc.execute(method, local_time_id, published_max=data["published-max"],
                              published_min=data["published-min"], updated_max=data["updated-max"],
                              updated_min=data["updated-min"], max_results=data["max-results"],
                              start_index=data["start-index"], depth=data["depth"])

    # Meter Reading Endpoints: GET Requests
    elif "meter_submit" in data:
        meter_id = id_check(data, "meter_id")
        if "sub_id" in data:
            method = "meter_reading_subscription_usage"
            if "meter_id" in data:
                response = gc.execute(method, data["sub_id"], data["usage_id"], meter_id=meter_id,
                                      published_max=data["published-max"], published_min=data["published-min"],
                                      updated_max=data["updated-max"], updated_min=data["updated-min"],
                                      max_results=data["max-results"], start_index=data["start-index"],
                                      depth=data["depth"])
        else:
            method = "meter_reading"
            response = gc.execute(method, meter_id, published_max=data["published-max"],
                                  published_min=data["published-min"], updated_max=data["updated-max"],
                                  updated_min=data["updated-min"], max_results=data["max-results"],
                                  start_index=data["start-index"], depth=data["depth"])

    # Reading Type Endpoints: GET Requests
    elif "reading_type_submit" in data:
        reading_type_id = id_check(data, "reading_type_id")
        method = "reading_type"
        response = gc.execute(method, reading_type_id=reading_type_id, published_max=data["published-max"],
                              published_min=data["published-min"], updated_max=data["updated-max"],
                              updated_min=data["updated-min"], max_results=data["max-results"],
                              start_index=data["start-index"], depth=data["depth"])

    # Service Status Endpoint: GET Request
    elif "server_status_submit" in data:
        method = "service_status"
        response = gc.execute(method)

    # UsagePoint Endpoints: GET Requests
    elif "usagepoint_submit" in data:
        usage_id = id_check(data, "usage_id")
        if "sub_id" in data:
            method = "usage_by_subscription"
            if "usage_id" in data:
                response = gc.execute(method, data["sub_id"], usage_point_id=usage_id,
                                      published_max=data["published-max"], published_min=data["published-min"],
                                      updated_max=data["updated-max"], updated_min=data["updated-min"],
                                      max_results=data["max-results"], start_index=data["start-index"],
                                      depth=data["depth"])
        else:
            method = "usage"
            response = gc.execute(method, usage_point_id=usage_id, published_max=data["published-max"],
                                  published_min=data["published-min"], updated_max=data["updated-max"],
                                  updated_min=data["updated-min"], max_results=data["max-results"],
                                  start_index=data["start-index"], depth=data["depth"])
    if response is not None:
        try:
            context["response"] = response
            try:
                filename = "app/xml/" + method + ".xml"
                xml_file = open(filename, "w")
                for line in response:
                    xml_file.write(line)
            except ValueError:
                print("No XML file saved")
            try:
                xml = ParseXml(response)
                api_data = xml.parse()
                context["data_json"] = api_data
                context["api_data"] = json.dumps(api_data)
            except:
                print("Problem with parsing XML response.")
        except ValueError:
            print("Context does not exist")

    if context != {}:
        return render_template("index.html", **context)
    else:
        print("Has NO Context")
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
