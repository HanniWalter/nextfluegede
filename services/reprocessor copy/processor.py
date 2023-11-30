import json
import os

intern_primary_key = 0


def get_intern_primary_key():
    global intern_primary_key
    intern_primary_key += 1
    return intern_primary_key


dir_path = os.path.dirname(os.path.realpath(__file__))
filter_data_path = os.path.join(dir_path, 'filter_data.json')
with open(filter_data_path) as f:
    filter_data = json.load(f)["filter_data"]


def process_segment(raw_segment):
    return raw_segment


def process_leg(raw_leg):
    carriers = raw_leg["carriers"]  # what is that?
    duration = raw_leg["duration"]
    nights = raw_leg["nights"]
    raw_segments = raw_leg["segments"]
    if len(raw_segments) >= filter_data["max_segments"]:
        return None
    leg = {}
    leg["carriers"] = carriers
    leg["duration"] = duration
    leg["nights"] = nights
    leg["segments"] = raw_segments
    return leg


def process_result(raw_result, expiration_time):
    price_components = raw_result["price-components"]
    result = {}
    result["expiration-time"] = expiration_time
    result["price-components"] = price_components
    result["id"] = get_intern_primary_key()
    raw_itinerary = raw_result["_itinerary"]
    carriers = raw_itinerary["carriers"]
    provider = raw_itinerary["provider"]
    raw_legs = raw_itinerary["legs"]
    legs = []
    for raw_leg in raw_legs:
        leg = process_leg(raw_leg)
        if leg is None:
            return None
        legs.append(leg)
    _itinerary = {}
    _itinerary["carriers"] = carriers
    _itinerary["provider"] = provider
    _itinerary["legs"] = legs

    result["_itinerary"] = _itinerary
    return result


def process(data):
    metadata = {}
    metadata["search-parameters"] = data["search-parameters"]
    metadata["pricing-parameters"] = data["pricing-parameters"]
    metadata["parameter-hash"] = data["parameter-hash"]
    metadata["user-id"] = data["user-id"]
    expiration_time = data["expiration-time"]
    metadata["results-origin"] = "provider"

    raw_results = data["results"]["result"]
    results = []
    for raw_result in raw_results:
        result = process_result(raw_result, expiration_time=expiration_time)
        if result is not None:
            results.append(result)
    ret = metadata
    ret["results"] = results
    return ret


if __name__ == '__main__':
    with open('services/reprocessor/testdata.json') as f:
        data = json.load(f)
        processed = process(data)
        print(processed)
