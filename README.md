# High-Traffic Chatbot Microservice 🌟

Welcome to the High-Traffic Chatbot Microservice project! This repository contains the implementation of a robust backend service designed to handle massive message flows in a simulated high-traffic environment. The system leverages Python and RabbitMQ to ensure reliability, scalability, and performance.

## Introduction
This project simulates a high-traffic chatbot environment where users send queries to a backend system, and the system processes and responds to each message efficiently.

Key objectives:

- Handle high message volumes.
- Ensure reliable processing with RabbitMQ.
- Provide scalable solutions for real-world use cases.

# Getting Started

## Prerequisites
- Python 3.8 or higher
- RabbitMQ installed and running locally
## Setup
1. Clone the repository:
```git clone https://github.com/your-repo-name.git](https://github.com/desims/python-rabbitmq.git```
```cd your-repo-name```
3. Install dependencies:
pip install -r requirements.txt
4. Start RabbitMQ on your local machine.
   
## Run the Producer
```python send.py```

## Run the Consumer
```python receive.py```

# Implementation
## Message Producer
- Publishes messages to a fanout exchange in RabbitMQ.
- Simulates high-traffic with randomized and sequential messages.

```python
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
```
## Message Consumer
- Listens to the queue and processes incoming messages.
- Provides chatbot-like responses based on messages map:
   "Hello" → "Hi there! 😊"
   "Tell me a joke" → "Why did the chicken cross the road? To get to the other side! 😂"
```python
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
```
# Scalability Enhancements
- Database Integration: Store processed messages for future analytics using MongoDB
```python
# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "chat_service"
COLLECTION_NAME = "message_history"

def save_message_to_db(user_message, bot_response):
    """
    Save the processed message to MongoDB.
    """
    if not service_health["mongodb_connected"]:
        logging.error("Cannot save message: MongoDB is not connected.")
        return

    try:
        message = {
            "user_message": user_message,
            "bot_response": bot_response,
            "timestamp": datetime.now()
        }
        message_collection.insert_one(message)
        logging.info("Message saved to MongoDB.")
    except Exception as e:
        logging.error(f"Failed to save message to MongoDB: {e}")
```
