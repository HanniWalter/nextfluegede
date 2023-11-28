import os
import pika
import requests
import json
import redis
import datetime
import custom_db_connection
from pika.exchange_type import ExchangeType


def get_redis_client():
    redis_host = 'localhost'
    redis_port = 6379
    redis_db = 0
    return redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)


redis_client = get_redis_client()



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

def publish_result(data):
    channel = rabbitmq_channel()
    channel.exchange_declare(exchange='results',
                             exchange_type=ExchangeType.direct)
    b = channel.basic_publish(exchange='results',
                              routing_key='wrongprice',
                              body=json.dumps(data)
                              )
    print("published data; parameter_hash:", data["parameter-hash"] )

def on_filght_recived(ch, method, properties, body):
    print("search recived")
    data = json.loads(body)
    parameter_hash = data["parameter-hash"]
    results = custom_db_connection.get_data(parameter_hash)
    data["results"] = results
    publish_result(data)

def on_result_recived(ch, method, properties, body):
    
    data = json.loads(body)
    print("result recived", data["parameter-hash"], len(data["results"]))
    custom_db_connection.add_data(data)

def main():
    channel = rabbitmq_channel()
    
    channel.exchange_declare(exchange='searchflight', exchange_type= ExchangeType.direct)
    queue = channel.queue_declare(queue='cachequeue')
    channel.queue_bind(exchange='searchflight', queue=queue.method.queue, routing_key='fullsearch')
    channel.basic_consume(queue=queue.method.queue , on_message_callback= on_filght_recived, auto_ack=True)
    
    channel.exchange_declare(exchange='results', exchange_type=ExchangeType.direct)
    results_queue = channel.queue_declare(queue='rightprice_cache')
    channel.queue_bind(exchange='results', queue=results_queue.method.queue, routing_key='rightprice')
    channel.basic_consume(queue=results_queue.method.queue, on_message_callback=on_result_recived, auto_ack=True)    
    
    channel.start_consuming()



if __name__ == "__main__":
    print("Starting cache service")
    main()
