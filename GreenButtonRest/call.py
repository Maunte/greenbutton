import requests

import xml.etree.ElementTree as ET

from .clients_deprecated import GreenButtonClient as GBC


def main():
    args = [] # Required parameters go here
    params = {} # Optional parameters go here
    endpoint = "/espi/1_1/resource/ApplicationInformation" # Check clients_deprecated.py for reference
    app_info = GBC("Bearer 2a85f4bd-30db-4b7d-8f41-b046b0566cb3", endpoint, *args, **params)
    # other(app_info)
    result = app_info.execute()
    print(app_info.url)
    print(result)


def api_call(*args, **kwargs):
    return


def other(object):
    response = requests.request("GET", object.url, headers=object.headers)
    # / api / response?id = 5 & param = 9
    root = ET.fromstring(response.text)

    for child in root:
        print(child.tag)


if __name__ == '__main__':
    main()
