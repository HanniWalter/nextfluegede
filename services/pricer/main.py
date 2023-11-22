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

def on_wrong_price_recived(ch, method, properties, body):
    data = json.loads(body)
    data = pricing.get_price(data)
    publish_data(data)
    
channel = rabbitmq_channel()

def publish_data(data):
    channel.exchange_declare(exchange='results',
                             exchange_type=ExchangeType.direct)
    b = channel.basic_publish(exchange='results',
                              routing_key='rightprice',
                              body=json.dumps(data)
                              )
    print("published data; parameter_hash:", data["parameter-hash"] ) 


def main():
    channel = rabbitmq_channel()
    channel.exchange_declare(exchange='results', exchange_type= ExchangeType.direct)
    queue = channel.queue_declare(queue='wrongprice_pricer')
    channel.queue_bind(exchange='results', queue=queue.method.queue, routing_key='wrongprice')
    channel.basic_consume(queue=queue.method.queue , on_message_callback= on_wrong_price_recived, auto_ack=True)
    channel.start_consuming() 

if __name__ == "__main__":
    print("Starting provider manager")
    main()
