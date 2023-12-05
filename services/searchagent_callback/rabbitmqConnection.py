import pika
from pika.exchange_type import ExchangeType
import json
import os


class RabbitMQConnection:

    def rabbitmq_connection(self):
        service_name = "rabbitmqservice"
        port_name = "amqp"

        # Construct the environment variable names
        service_host_env_var = f"{service_name.upper()}_SERVICE_HOST"
        service_port_env_var = f"{service_name.upper()}_SERVICE_PORT_{port_name.upper()}"

        # Access the values from environment variables
        service_host = os.environ.get(service_host_env_var)
        service_port = os.environ.get(service_port_env_var)
        connection_params = pika.ConnectionParameters(
            service_host, service_port)
        print(f"Connecting to RabbitMQ on {service_host}:{service_port}")
        connection = pika.BlockingConnection(connection_params)
        return connection

    def publish_search(self, data):
        self.connection = self.rabbitmq_connection()
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange='searchflight', exchange_type=ExchangeType.fanout)
        b = self.channel.basic_publish(
            exchange='searchflight', routing_key='', body=json.dumps(data))
        print("published data; parameter_hash:", data["parameter-hash"])
        self.connection.close()

    def publish_results_for_pricer(self, search, results):
        data = search
        data["results"] = {}
        data["results"]["result"] = results
        self.connection = self.rabbitmq_connection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='pricer')
        b = self.channel.basic_publish(
            exchange='', routing_key='pricer', body=json.dumps(data))
        print("published data to pricer; parameter_hash:",
              data["parameter-hash"])
        self.connection.close()
        pass
