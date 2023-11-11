import zlib
from flask import Flask, jsonify, request, abort

app = Flask(__name__)


class Flight():
    def __init__(self, json) -> None:
        self._valid = True
        self.adults = json["adults"]
        self.children = json["children"]
        self.infants = json["infants"]
        class_filter = [x.upper() for x in json["filter-cabin-class"]]
        self.economy = ("ECONOMY" in class_filter)
        self.premium_economy = ("PREMIUM ECONOMY" in class_filter)
        self.buisness = ("BUISNESS" in class_filter)
        self.first = ("FIRST" in class_filter)

        self.request_type = json["request-type"]

        if self.request_type not in ["single-trip", "round-trip", "open-jaw"]:
            self.valid = False
        legs = [self.legToString(leg) for leg in json["legs"]]
        self.legs = sorted(legs)

    def toString(self):
        return f"[{self.request_type}];[{self.adults};{self.children};{self.infants}];[{str(self.economy).upper()};{str(self.premium_economy).upper()};{str(self.buisness).upper()};{str(self.first).upper()}];[{';'.join( self.legs )}]"

    def legToString(self, leg):
        return "("+leg["depart-at"] + ";" + leg["departure"].upper()+";" + leg["arrival"].upper() + ";" + str(leg["is-flexible-date"]).upper()+")"

    def toHash(self):
        return zlib.adler32(bytes(self.toString(), "utf-8"))


@app.route("/hash", methods=["POST"])
def searchflights():
    if request.method == "POST":
        #      try:
        if not request.is_json:
            abort(415, description='Unsupported Media Type: Did not receive JSON data.')

        # Get JSON data from the request
        json_data = request.get_json()

        # Create a Flight instance
        flight_instance = Flight(json_data["search-parameters"])
        if not flight_instance._valid:
            abort(400, description="parameters are invalid")

        # Calculate and return the hash
        result_hash = flight_instance.toHash()

        return jsonify({'hash': result_hash})

#      except Exception as e:
#        abort(500, description=str(e))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5110)
