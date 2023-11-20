from flask import Flask, jsonify, request, abort
import os
import pika
import json
import processor

app = Flask(__name__)


def rabbitmq_channel():
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
    return channel


rabbitmq_channel = rabbitmq_channel()


@app.route("/reprocessor/", methods=["PUT"])
def reprocessor():
    # print request body
    processed_result = processor.process(request.json)

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


def publish_data(data):
    ra


def main():
    rabbitmq = rabbitmq_channel()
    app.run(debug=True, host='0.0.0.0', port=5111)


if __name__ == "__main__":
    print("starting reprocessor")
    main()
