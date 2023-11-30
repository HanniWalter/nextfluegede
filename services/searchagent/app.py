from flask import Flask, jsonify, request, abort
import agent
app = Flask(__name__)


@app.route("/registersearch/", methods=["PUT"])
def reprocessor():
    pass

def register_search(search):

def main():
    app.run(debug=True, host='0.0.0.0', port=5102)


if __name__ == "__main__":
    print("starting reprocessor")
    main()
