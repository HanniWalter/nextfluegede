import pika
import os
from pika.exchange_type import ExchangeType


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
                          on_message_callback=callback)
    print("registered callback")
    channel.start_consuming()


def callback(ch, method, properties, body):
    print(properties)
    print(body.keys())


if __name__ == "__main__":
    print("starting consumer")
    main()
