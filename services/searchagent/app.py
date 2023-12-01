from flask import Flask, jsonify, request, abort
import agent
app = Flask(__name__)


@app.route('/search/', methods=['POST'])
def register_search():
    body = request.json
    agent.registerSearch(body)
    return jsonify({"status": "ok"})


@app.route('/search', methods=['GET'])
def get_search():
    body = request.json
    print(body)


@app.route('/teapot', methods=['GET'])
def teapot():
    abort(418)


def main():
    app.run(debug=True, host='0.0.0.0', port=5102)


if __name__ == "__main__":
    print("starting searchagent")
    main()
