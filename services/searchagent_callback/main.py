import pika
import os
from pika.exchange_type import ExchangeType
import json
import agent


def rabbitmq_connection():
    service_name = "rabbitmqservice"
    port_name = "amqp"
    # Construct the environment variable names
    service_host_env_var = f"{service_name.upper()}_SERVICE_HOST"
    service_port_env_var = f"{service_name.upper()}_SERVICE_PORT_{port_name.upper()}"
    # Access the values from environment variables
    service_host = os.environ.get(service_host_env_var)
    service_port = os.environ.get(service_port_env_var)
    connection_params = pika.ConnectionParameters(
        service_host, service_port)
    print(f"Connecting to RabbitMQ on {service_host}:{service_port}")
    connection = pika.BlockingConnection(connection_params)
    return connection


def main():
    connection = rabbitmq_connection()
    channel = connection.channel()

    channel.exchange_declare(
        exchange='results', exchange_type=ExchangeType.topic)
    queue = channel.queue_declare(queue='', exclusive=True)
    channel.queue_bind(
        exchange='results', queue=queue.method.queue, routing_key='results.#')
    channel.basic_consume(queue=queue.method.queue, auto_ack=True,
                          on_message_callback=on_result_received)
    print("registered callback")
    channel.start_consuming()


def on_result_received(ch, method, properties, body):
    print("received result")
    body = json.loads(body)
    if "error" in body:
        print("no data from", body['provider-name'])
    else:
        if body["results-origin"] == "provider":
            print("data from", body["results-origin"],
                  body['results-provider-name'])
            agent.registerResult(body)
        elif body["results-origin"] == "cache":
            print("data from", body["results-origin"],
                  body['results-provider-name'])
            agent.registerResult(body)
        elif body["results-origin"] == "pricer":
            print("data from", body["results-origin"])
            agent.registerPricedResult(body)
        else:
            print("unknown origin", body["results-origin"])


if __name__ == "__main__":
    print("starting consumer")
    main()
