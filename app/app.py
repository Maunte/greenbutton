import os

from flask import Flask, render_template, request

from flask.views import MethodView

from GreenButtonRest.clients import GreenButtonClient as gbc

app = Flask(__name__)

app.config.update(dict(
    WTF_CSRF_ENABLED = True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('APP_SETTINGS', silent=True)


@app.route("/", methods=['GET', 'POST'])
def main():
    data = request.form
    if "access_token" in request.form:
        token = data["access_token"]
        print token
        args = []
        kwargs = {}
        if "app_info_submit" in request.form:
            endpoint = "/espi/1_1/resource/ApplicationInformation"
            for key, value in data.iteritems():
                if value != "" and key != "access_token":
                    kwargs[key] = value
        elif "app_info_id_submit" in data:
            endpoint = "/espi/1_1/resource/ApplicationInformation"
            args.append(data["app_info_id"])
        else:
            print "No endpoint defined!"

        call = gbc(token, endpoint, *args, **kwargs)
        print call.url
        response = call.execute()
        print response

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
