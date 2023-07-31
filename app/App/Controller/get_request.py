import pika
from App.Controller.process import process
from App import config
import sys
import os

def main():
    host = config.configs['RABBITMQ_SERVICE_NAME']
    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel = connection.channel()

    # It will create a queue if doesn't exist. To be sure there is queue
    channel.queue_declare(queue='requests')

    # Whenever we receive a message, this callback function is called
    def callback(ch, method, properties, body):        
        proc_res = process(int(body.decode()))
        return proc_res

    channel.basic_consume(queue='requests', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()
    

# receive request from queue 
def get_requests_from_queue():
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    