
import pika
import threading
import json
from datetime import datetime

# RabbitMQ configuration
RABBITMQ_HOST = "localhost"
EXCHANGE_NAME = "chat_exchange"

# Message response map
RESPONSES = {
    "Hello": "Hi there! 😊",
    "Tell me about weather": "The weather is sunny and bright! ☀️",
    "Tell me a joke": "Why did the chicken cross the road? To get to the other side! 😂",
    "What's the time?": "Sorry, I can't tell the exact time right now! ⏰"
}

def process_message(body):
    
    #Process an incoming message and respond.
    message = json.loads(body.decode("utf-8"))
    user_message = message.get("message", "")

    response_text = RESPONSES.get(user_message, "Sorry, I'm not sure how to respond to that. 🤔")

    response = {
        "from": "bot",
        "message": response_text,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # print(f"Received: {message} | Responded: {response}")
    print(f"Received: {message}")
    print(f"Responded: {response}\n")

def callback(channel, method, properties, body):
    
    threading.Thread(target=process_message, args=(body,)).start()
    # Acknowledge the message
    channel.basic_ack(delivery_tag=method.delivery_tag)
    

def main():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # Declare a temporary queue to bind to the exchange
    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue

    # Bind the queue to the exchange
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name)

    print("Chatbot is ready and listening for messages...")
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Stopping the chatbot...")
        connection.close()

if __name__ == "__main__":
    main()