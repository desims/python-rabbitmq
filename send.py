import pika
import json
import time
from datetime import datetime
from random import choice

# RabbitMQ configuration
RABBITMQ_HOST = "localhost"
EXCHANGE_NAME = "chat_exchange"
MESSAGES = ["Hello", "Tell me about weather", "Tell me a joke", "How's it going?", "What's the time?"]

def main():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # Declare a fanout exchange
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="fanout")

    print("Starting to send messages...")
    while True:
        # Create a simple random message
        message = {
            "from":"user",
            "message": choice(MESSAGES), 
            "date":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        message_body = json.dumps(message)

        # Publish to the fanout exchange
        channel.basic_publish(exchange=EXCHANGE_NAME, routing_key="", body=message_body)
        print(f"Sent: {message}")

        # Simulate high traffic
        time.sleep(0.5)

    connection.close()

if __name__ == "__main__":
    main()
