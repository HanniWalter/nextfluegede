import os
import json
from flask import Flask, render_template, jsonify, request, abort
import logging
import pika

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template('index.html')


@app.route("/searchflight", methods=["POST"])
def searchflights():
    if request.method == "POST":
        value = request.get_json()
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')

        queue_name = 'searchflight'
        channel.queue_declare(queue=queue_name)
        message = 'Hello, RabbitMQ!'
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=message)

        # logic
        # headers = {'Content-Type': 'application/json'}
        # data = {
        #    "flightdata": "your_flight_data",
        #    "websessionid": "your_websession_id"
        # }
        # data = json.dump(data)
        return response


@app.route("/teapot")
def teapot():
    return abort(418)


if __name__ == '__main__':
    service_name = "rabbitmqservice"
    port_name = "amqp"

    # Construct the environment variable names
    service_host_env_var = f"{service_name.upper()}_SERVICE_HOST"
    service_port_env_var = f"{service_name.upper()}_SERVICE_PORT_{port_name.upper()}"

    # Access the values from environment variables
    service_host = os.environ.get(service_host_env_var)
    service_port = os.environ.get(service_port_env_var)
    connection_params = pika.ConnectionParameters(service_host, service_port)
    print(f"Connecting to RabbitMQ on {service_host}:{service_port}")
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    app.run(host='0.0.0.0', port=5101)
