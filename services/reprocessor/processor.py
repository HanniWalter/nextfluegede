import json
import os

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


def process_result(raw_result):
    price_components = raw_result["price-components"]
    result = {}
    result["price-components"] = price_components
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
    raw_results = data["results"]["result"]
    results = []
    for raw_result in raw_results:
        result = process_result(raw_result)
        if result is not None:
            results.append(result)
    return results


if __name__ == '__main__':
    with open('services/reprocessor/testdata.json') as f:
        data = json.load(f)
        processed = process(data)
        print(processed)
