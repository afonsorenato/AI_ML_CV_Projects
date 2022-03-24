import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Connected toa broker on the local machine - local host
# If wanted to connect to other machine - put its IP address

# Creates the queue
channel.queue_declare(queue='hello')


message_to_send = 'Hello world'

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message_to_send)

print(" [x] Sent 'Hello World!'")

connection.close()
