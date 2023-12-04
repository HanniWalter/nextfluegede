from flask import Flask, jsonify, request, abort
import os
import pika
import json
import processor
from pika.exchange_type import ExchangeType

app = Flask(__name__)


def rabbitmq_connection():
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
    return connection


@app.route("/reprocessor/", methods=["PUT"])
def reprocessor():
    processed_result = processor.process(request.json)
    publish_data(processed_result)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


def publish_data(data):
    provider_name = data["results-provider-name"][0]

    connection = rabbitmq_connection()
    channel = connection.channel()
    channel.exchange_declare(
        exchange='results', exchange_type=ExchangeType.topic)

    b = channel.basic_publish(exchange='results',
                              routing_key='results.'+str(data["parameter-hash"])+'.provider.'+provider_name+".success", body=json.dumps(data))
    print("publishing data; parameter_hash:", data["parameter-hash"])
    connection.close()


def main():
    app.run(debug=True, host='0.0.0.0', port=5111)


if __name__ == "__main__":
    main()
