import os
import pika
import time
import threading
import random
import json
import requests
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
    connection_params = pika.ConnectionParameters(service_host, service_port)
    print(f"Connecting to RabbitMQ on {service_host}:{service_port}")
    connection = pika.BlockingConnection(connection_params)
    return connection


def get_search(userid):
    search = {}
    with open("searches/001.json", 'r') as file:
        search_parameters = json.load(file)
    with open("users/001.json", 'r') as file:
        pricing_parameters = json.load(file)
    search["search-parameters"] = search_parameters["search-parameters"]
    search["pricing-parameters"] = pricing_parameters["pricing-parameters"]
    headers = {'Content-Type': 'application/json'}
    response = requests.post("http://localhost:5110/hash",
                             json=search)
    search["parameter-hash"] = response.json()["hash"]
    search["user-id"] = userid
    return search


def send_searches(rabbitmq, userid):
    searchdict = get_search(userid=userid)
    channel = rabbitmq.channel()
    time.sleep(1)
    channel.exchange_declare(exchange='searchflight',
                             exchange_type=ExchangeType.direct)
    while True:
        # send message
        b = channel.basic_publish(exchange='searchflight',
                                  routing_key='fullsearch',
                                  body=json.dumps(searchdict)
                                  )
        print("send message")
        time.sleep(10)

def single_search(rabbitmq, userid):
    searchdict = get_search(userid)
    channel = rabbitmq.channel()
    time.sleep(1)
    channel.exchange_declare(exchange='searchflight',
                             exchange_type=ExchangeType.direct)
    # send message
    b = channel.basic_publish(exchange='searchflight',
                              routing_key='fullsearch',
                              body=json.dumps(searchdict)
                              )
    print("send dummy message")

def on_result_recived(ch, method, properties, body):
    data = json.loads(body)
    if data["user-id"] == 41:
        print("result recived")
        print(data)

def single_search_check_results(rabbitmq):
    channel = rabbitmq.channel()
    channel.exchange_declare(exchange='results',
                             exchange_type=ExchangeType.direct)
    queue = channel.queue_declare(queue='search_simulator')
    channel.queue_bind(exchange='results', queue=queue.method.queue, routing_key='rightprice')
    channel.basic_consume(queue=queue.method.queue , on_message_callback= on_result_recived, auto_ack=True)
    channel.start_consuming()

def main():
    userId = 1
    rabbitmq = rabbitmq_connection()

    time.sleep(8)
    single_search(rabbitmq=rabbitmq, userid=41)
    single_search_check_results(rabbitmq=rabbitmq)
    while True:
        pass    

    rabbitmq.close()

if __name__ == "__main__":
    print("Starting provider manager")
    main()
