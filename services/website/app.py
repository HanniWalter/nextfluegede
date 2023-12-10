import os
import json
from flask import Flask, render_template, jsonify, request, abort
import logging
import requests
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


def convert_date_format(input_date_string):
    # Convert the input string to a datetime object
    input_date = datetime.strptime(input_date_string, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Format the datetime object as a string in the desired format
    output_date_string = input_date.strftime("%Y-%m-%d")

    return output_date_string


def get_search(data, userid):
    search = {}
    search_parameters = {}
    search_parameters["adults"] = int(data["search"]["adults"])
    search_parameters["children"] = int(data["search"]["children"])
    search_parameters["infants"] = int(data["search"]["infants"])
    search_parameters["agent"] = "fluege.de"
    search_parameters["filter-cabin-class"] = [data["search"]["flight_class"]]
    if data["search"]["flight_type"] == "single":
        search_parameters["request-type"] = "single"
        search_parameters["legs"] = [
            {"depart-at": convert_date_format(data["search"]["date"]),
             "is-flexible-date": data["search"]["flexdate"],
             "departure": data["search"]["from"],
             "arrival": data["search"]["to"]
             }
        ]
    if data["search"]["flight_type"] == "double":
        search_parameters["request-type"] = "double"
        search_parameters["legs"] = [
            {"depart-at": convert_date_format(data["search"]["date1"]),
             "is-flexible-date": data["search"]["flexdate1"],
             "departure": data["search"]["from"],
             "arrival": data["search"]["to"]
             },
            {"depart-at": convert_date_format(data["search"]["date2"]),
             "is-flexible-date": data["search"]["flexdate2"],
             "departure": data["search"]["to"],
             "arrival": data["search"]["from"]
             }
        ]
    if data["search"]["flight_type"] == "open_jaw":
        search_parameters["request-type"] = "open_jaw"
        search_parameters["legs"] = [
            {"depart-at": convert_date_format(data["search"]["date1"]),
             "is-flexible-date": data["search"]["flexdate1"],
             "departure": data["search"]["from1"],
             "arrival": data["search"]["to1"]
             },
            {"depart-at": convert_date_format(data["search"]["date2"]),
             "is-flexible-date": data["search"]["flexdate2"],
             "departure": data["search"]["from2"],
             "arrival": data["search"]["to2"]
             }
        ]
    pricing_parameters = {}
    pricing_parameters["curency"] = "EUR"
    pricing_parameters["fee_flat"] = 0
    pricing_parameters["fee"] = 0.1
    pricing_parameters["price_type"] = "NORMAL"

    pricing_parameters["user_type"] = data["user"]["user_type"]
    pricing_parameters["device_type"] = data["user"]["device_type"]

    search["search-parameters"] = search_parameters
    search["pricing-parameters"] = pricing_parameters
    headers = {'Content-Type': 'application/json'}

    search["user-id"] = userid
    return search


@app.route("/")
def main_page():
    return render_template('index.html')


@app.route("/searchflight/", methods=["GET", "POST"])
def searchflights():
    if request.method == "POST":
        searchagent_service_url = "http://localhost:5102"
        value = request.get_json()
        search = get_search(value, 42)
        print(search)
        r = requests.post(searchagent_service_url+"/search/", json=search)

        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response

    if request.method == "GET":
        searchdict = get_mock_search(userid=42)
        searchagent_service_url = "http://localhost:5102"
        r = requests.get(searchagent_service_url+"/search/", json=searchdict)
        response = jsonify(r.json())
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response


@app.route("/teapot")
def teapot():
    return abort(418)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5101)
