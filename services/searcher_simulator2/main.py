import time
import json
import requests


def get_search(userid):
    search = {}
    with open("searches/001.json", 'r') as file:
        search_parameters = json.load(file)
    with open("users/001.json", 'r') as file:
        pricing_parameters = json.load(file)
    search["search-parameters"] = search_parameters["search-parameters"]
    search["pricing-parameters"] = pricing_parameters["pricing-parameters"]
    headers = {'Content-Type': 'application/json'}

    search["user-id"] = userid
    return search


def single_search(userid):
    searchdict = get_search(userid)
    time.sleep(8)
    print("Sending search")
    searchagent_service_url = "http://searchagentservice:5102"
    requests.post(searchagent_service_url+"/search/", json=searchdict)


def get_results(userid):
    searchdict = get_search(userid)
    searchagent_service_url = "http://searchagentservice:5102"
    r = requests.get(searchagent_service_url+"/search/", json=searchdict)
    print(r.json())


def main():
    userId = 1

    time.sleep(2)
    single_search(userid=43)
    while True:
        time.sleep(2)
        get_results(userid=43)
        pass


if __name__ == "__main__":
    print("Starting test search manager")
    main()
