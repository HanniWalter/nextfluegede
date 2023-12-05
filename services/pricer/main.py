import os
import pika
import json
import datetime
from pika.exchange_type import ExchangeType
import pricing


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


def on_data_recived(ch, method, properties, body):
    data = json.loads(body)
    data = pricing.get_price(data)
    publish_data(data)


channel = rabbitmq_channel()


def publish_data(data):
    data["results-origin"] = "pricer"
    channel.exchange_declare(
        exchange='results', exchange_type=ExchangeType.topic)
    b = channel.basic_publish(exchange='results',
                              routing_key='results.'+str(data["parameter-hash"])+'.pricer.success', body=json.dumps(data))
    print("published data; parameter_hash:", data["parameter-hash"])


def main():
    channel.queue_declare(queue='pricer')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue='pricer', on_message_callback=on_data_recived, auto_ack=True)
    channel.start_consuming()


if __name__ == "__main__":
    print("Starting provider manager")
    main()
