import pika
from pika.exchange_type import ExchangeType

class RabbitMQConnection:
    def __init__(self):
        self.channel = self.rabbitmq_connection().channel()
    
    def rabbitmq_connection(self):
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
    
    def publish_search(self, data):
        self.channel.exchange_declare(exchange='searchflight', exchange_type= ExchangeType.direct)
        b = self.channel.basic_publish(exchange='searchflight', routing_key='fullsearch', body=json.dumps(data))
        print("published data; parameter_hash:", data["parameter-hash"] )

    def register_result_callback(self, callback):
        pass

