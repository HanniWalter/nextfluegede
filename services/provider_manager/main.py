import os
import pika
import requests
import json
import redis 
import datetime

def read_provider_json():
    with open('providerinfo.json', 'r') as file:
        data = json.load(file)
    return data

def get_redis_client():
    redis_host = 'localhost'
    redis_port = 6379
    redis_db = 0
    return redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

redis_client = get_redis_client()
provider_info = read_provider_json()["provider"]

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

def get_results(search_parameter):
    search = {}
    search["search-parameters"] = search_parameter["search-parameters"]
    
    #todo remove hardcoding
    search["mock-options"] =  {}
    search["mock-options"][""] = 500 
    search["mock-options"]["max-results"] = provider_info["max-results"]
    search["mock-options"]["provider"] = provider_info["name"]

    response = requests.post(provider_info["address"] ,json=search)
    response = response.json()
    return response

    #send response to enrichment

def main():
    rabbitmq = rabbitmq_channel()

    while True:
        queue_name = 'searchflight'
        rabbitmq.queue_declare(queue=queue_name)
        method_frame, header_frame, body = rabbitmq.basic_get(queue=queue_name)
        if method_frame:
            rabbitmq.basic_ack(method_frame.delivery_tag)
            search = json.loads(body)
            hash = search["parameter-hash"]
            if redis_client.exists(hash):
                print("refuse to work, hash already known", hash)
            else:
                current_datetime = datetime.datetime.now()
                expiration_date = current_datetime + datetime.timedelta(seconds= provider_info["ttl"])
                results = get_results(search)
                process_results(results, search, expiration_date)

                redis_client.set(hash, "")
                redis_client.expireat(hash, expiration_date)
                print("worked, hash is now known", hash)

def process_results(results, search, expiration_time):
    process_dict = search
    process_dict["results"] = results
    #process_dict["search"] = search
    #to iso
    process_dict["expiration-time"] = expiration_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
    
    reprocessor_service_url = "http://reprocessorservice:5111" 
    response = requests.put(f"{reprocessor_service_url}/reprocessor/", json=process_dict)
    # return true if success status code
    return response.status_code == 200

if __name__ == "__main__":
    print("Starting provider manager")
    main()
