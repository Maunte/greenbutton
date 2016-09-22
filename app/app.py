import os

from flask import Flask, render_template, request

from GreenButtonRest.clients import GreenButtonClient as gbc

app = Flask(__name__)

app.config.update(dict(
    WTF_CSRF_ENABLED=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('APP_SETTINGS', silent=True)


def fill_kwargs(data, *exclude):
    kwargs = {}
    for key, value in data.iteritems():
        if key not in exclude and value != "":
            kwargs[key] = value
    return kwargs


@app.route("/", methods=['GET', 'POST'])
def main():
    data = request.form
    if "access_token" in request.form:
        token = data["access_token"]
        args, kwargs = [], {}
        if "app_info_submit" in request.form:
            endpoint = "/espi/1_1/resource/ApplicationInformation"
            kwargs = fill_kwargs(data, "access_token" )
        elif "app_info_id_submit" in data:
            endpoint = "/espi/1_1/resource/ApplicationInformation"
            args.append(data["app_info_id"])
        elif "auth_submit" in data:
            endpoint = "/espi/1_1/resource/Authorization"
            if "auth_id" in data:
                args.append(data["auth_id"])
            kwargs = fill_kwargs(data, "access_token", "auth_info_id")
        elif "bulk_submit" in data:
            if "bulk_id" in data:
                endpoint = "/espi/1_1/resource/Batch/Bulk"
                args.append(data["bulk_id"])
            elif "bulk_sub_id" in data:
                endpoint = "/espi/1_1/resource/Batch/Subscription"
                args.append(data["bulk_sub_id"])
            elif "bulk_customer_id" in data:
                endpoint = "/espi/1_1/resource/Batch/RetailCustomer"
                args.append(data["bulk_customer_id"])
            elif "bulk_sub_usage_id" in data:
                endpoint = "/espi/1_1/resource/Batch/Subscription/UsagePoint"
                args.append(data["bulk_sub_id"])
            kwargs = fill_kwargs(data, "access_token","bulk_radio", "bulk_id", "bulk_sub_id", "bulk_customer_id",
                                 "bulk_sub_usage_id")
        else:
            print "No endpoint defined!"

        call = gbc(token, endpoint, *args, **kwargs)
        response = call.execute()
        print call.url
        print response

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
