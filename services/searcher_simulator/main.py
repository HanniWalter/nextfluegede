import os
import pika
import time
import threading

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

def send_messages(rabbitmq):
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
        print("send hello world", b)
        time.sleep(10)

def main():
    rabbitmq = rabbitmq_connection()
    # Create a thread to send messages in the background
    message_thread = threading.Thread(target=send_messages, args=(rabbitmq,))
    message_thread.start()
    
    while True:
        pass

    rabbitmq.close()

if __name__ == "__main__":
    print("Starting provider manager")
    main()
