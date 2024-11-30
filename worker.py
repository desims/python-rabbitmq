
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# channel.queue_declare(queue='hello')

# Create a durable queue
channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Fair dispatching
channel.basic_qos(prefetch_count=1)

# channel.basic_consume(queue='hello', on_message_callback=callback)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()
