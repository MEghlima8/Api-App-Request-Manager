import pika
from App import config

def send(val):
    host = config.configs['RABBITMQ_SERVICE_NAME']
    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel = connection.channel()

    channel.queue_declare(queue='requests')

    channel.basic_publish(exchange='', routing_key='requests', body=val)
    connection.close()
    
    return 'true'