import os
import pika


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


def main():
    rabbitmq = rabbitmq_channel()

    while True:
        queue_name = 'searchflight'
        rabbitmq.queue_declare(queue=queue_name)
        # get message
        method_frame, header_frame, body = rabbitmq.basic_get(queue=queue_name)
        if method_frame:
            print(method_frame, header_frame, body)
            rabbitmq.basic_ack(method_frame.delivery_tag)


if __name__ == "__main__":
    print("Starting provider manager")
    main()
