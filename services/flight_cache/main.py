import os
import pika
import requests
import json
import redis
import datetime
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



def on_filght_recived(ch, method, properties, body):
    print("search recived")
    #print(body)
            #    return
        #    if redis_client.exists(hash):
        #        print("refuse to work, hash already known", hash)
        #    else:
        #        current_datetime = datetime.datetime.now()
        #        expiration_date = current_datetime + \
        #            datetime.timedelta(seconds=provider_info["ttl"])
        #        results = get_results(search)
        #        process_results(results, search, expiration_date)

        #        redis_client.set(hash, "")
        #        redis_client.expireat(hash, expiration_date)
        #        print("worked, hash is now known", hash)

def on_result_recived(ch, method, properties, body):
    print("result recived")
    print(body)

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
