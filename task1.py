import pika
import json

# Configuration
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'chatbot_queue'

def connect_to_rabbitmq():
    """Establishes connection and channel to RabbitMQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    # Declare the queue to ensure it exists
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    return channel

def send_message(channel, message):
    """Sends a message to the queue."""
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make the message persistent
        ),
    )
    print(f"Sent: {message}")

def main():
    """Main function to produce messages."""
    channel = connect_to_rabbitmq()

    # Example messages
    messages = [
        {"id": 1, "user": "Alice", "message": "Hi! How are you?"},
        {"id": 2, "user": "Bob", "message": "Hello! Can you help me with my order?"},
    ]

    for msg in messages:
        send_message(channel, msg)

    print("All messages sent.")

if __name__ == "__main__":
    main()
