import os
import pika
import requests
import json
import redis
import datetime
from pika.exchange_type import ExchangeType


def read_provider_info():
    data = {}
    data["id"] = int(os.environ.get("PROVIDER_ID"))
    data["name"] = os.environ.get("PROVIDER_NAME")
    data["address"] = os.environ.get("PROVIDER_ADDRESS")
    data["max-results"] = int(os.environ.get("PROVIDER_MAX_RESULTS"))
    data["ttl"] = float(os.environ.get("PROVIDER_TTL"))
    return {"provider": data}


def get_redis_client():
    redis_host = 'localhost'
    redis_port = 6379
    redis_db = 0
    return redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)


redis_client = get_redis_client()
provider_info = read_provider_info()["provider"]


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


channel = rabbitmq_channel()


def get_results(search_parameter):
    search = {}
    search["search-parameters"] = search_parameter["search-parameters"]

    # todo remove hardcoding
    search["mock-options"] = {}
    search["mock-options"]["max-results"] = provider_info["max-results"]
    search["mock-options"]["provider"] = provider_info["name"]

    response = requests.post(provider_info["address"], json=search)
    response = response.json()
    return response


def on_filght_recived(ch, method, properties, body):
    search = json.loads(body)
    hash = search["parameter-hash"]
    if redis_client.exists(hash):
        print("refuse to work, hash already known", hash)
        refuse_results(hash)
    else:
        current_datetime = datetime.datetime.now()
        expiration_date = current_datetime + \
            datetime.timedelta(seconds=provider_info["ttl"])
        results = get_results(search)
        publish_results(results, search, expiration_date)
        redis_client.set(hash, "")
        redis_client.expireat(hash, expiration_date)
        print("worked, hash is now known", hash)


def refuse_results(hash):
    provider_name = provider_info["name"]

    channel.exchange_declare(
        exchange='results', exchange_type=ExchangeType.topic)

    b = channel.basic_publish(exchange='results',
                              routing_key='results.'+str(hash)+'.provider.'+provider_name+".refused", body=json.dumps({"error": "hash already known", "provider-name": provider_name}))


def main():

    channel.exchange_declare(exchange='searchflight',
                             exchange_type=ExchangeType.fanout)
    queue = channel.queue_declare(queue='', exclusive=True)
    channel.queue_bind(exchange='searchflight',
                       queue=queue.method.queue)
    channel.basic_consume(queue=queue.method.queue,
                          on_message_callback=on_filght_recived, auto_ack=True)
    channel.start_consuming()


def publish_results(results, search, expiration_time):
    process_dict = search
    process_dict["provider-name"] = provider_info["name"]
    process_dict["results"] = {}
    process_dict["results"] = results
    process_dict["expiration-time"] = expiration_time.strftime(
        "%Y-%m-%dT%H:%M:%S.%f")
    print("publishing results")

    reprocessor_service_url = "http://reprocessorservice:5111"
    response = requests.put(
        f"{reprocessor_service_url}/reprocessor/", json=process_dict)
    # return true if success status code
    return response.status_code == 200


if __name__ == "__main__":
    print("Starting provider manager")
    main()
