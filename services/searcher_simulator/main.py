import os
import pika
import time
import threading
import random
import json
import requests


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

#build a nice little search
def get_search(userid):
    search = {}
    with open("searches/001.json", 'r') as file:
        data_dict = json.load(file)


    search["search-parameters"] = data_dict["search-parameters"]
    
    response = requests.post("http://localhost:5110/hash", json= search)
    print(response)

    search["user-id"] = userid
    return search

def send_searches(rabbitmq, userid):
    searchdict = get_search(userid=userid)
    print(searchdict)
    
    channel = rabbitmq.channel()
    time.sleep(1)
    queue_name = 'searchflight'
    channel.queue_declare(queue=queue_name) 
    channel.confirm_delivery()
    while True:        
        # send message
        b =channel.basic_publish(exchange='',
                      routing_key=queue_name,
                      body='Hello World!')
        time.sleep(10)

def main():
    userId = random.randint(1, 1000000)
    #rabbitmq = rabbitmq_connection()
    rabbitmq = None
    # Create a thread to send messages in the background
    message_thread = threading.Thread(target=send_searches, args=(rabbitmq,userId))
    message_thread.start()
    
    while True:
        pass

    rabbitmq.close()

if __name__ == "__main__":
    print("Starting provider manager")
    main()
