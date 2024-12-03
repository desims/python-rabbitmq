
# # import pika, sys, os

# # def main():
# #     # Establish a connection with the RabbitMQ server
# #     connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# #     channel = connection.channel()

# #     # Redeclare the queue because we are unsure whether or not the queue exists. 
# #     channel.queue_declare(queue='hello')

# #     # RabbitMQ will trigger this function once we receive a message.
# #     def callback(ch, method, properties, body):
# #         print(f" [x] Received {body}")

# #     # Subscribe to the "hello" queue. 
# #     channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

# #     print(' [*] Waiting for messages. To exit press CTRL+C')
# #     channel.start_consuming()

# # if __name__ == '__main__':
# #     try:
# #         main()
# #     except KeyboardInterrupt:
# #         print('Interrupted')
# #         try:
# #             sys.exit(0)
# #         except SystemExit:
# #             os._exit(0)

# # Filename: chatbot_consumer.py

# import pika
# import threading
# import json
# import time

# # RabbitMQ Configuration
# RABBITMQ_HOST = 'localhost'
# EXCHANGE_NAME = 'chat_exchange'
# QUEUE_NAME = 'chat_queue'
# ROUTING_KEY = 'chat_message'

# # Predefined Responses
# RESPONSES = {
#     "Hello": "Hi there! 😊",
#     "Tell me about weather": "The weather is sunny and bright! ☀️",
#     "Tell me a joke": "Why did the chicken cross the road? To get to the other side! 😂"
# }

# def process_message(ch, method, properties, body):
#     """Processes incoming messages and sends a response."""
#     try:
#         message = json.loads(body)
#         query = message.get("query", "Unknown query")
#         response = RESPONSES.get(query, "I'm sorry, I don't understand that. 🤔")
        
#         # Simulate response processing time
#         time.sleep(0.5)
        
#         print(f"Received: {query}")
#         print(f"Responded: {response}")
#     except Exception as e:
#         print(f"Error processing message: {e}")
#     finally:
#         # Acknowledge message processing
#         ch.basic_ack(delivery_tag=method.delivery_tag)

# def start_consumer():
#     """Starts the RabbitMQ consumer."""
#     # Establish connection
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
#     channel = connection.channel()

#     # Declare queue and bind to exchange
#     channel.queue_declare(queue=QUEUE_NAME, durable=True)
#     channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=ROUTING_KEY)

#     print("Consumer is running. Waiting for messages...")
    
#     # Set up a basic consumer with concurrency using multiple threads
#     channel.basic_qos(prefetch_count=1)  # Process one message at a time per worker
#     channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_message)

#     try:
#         channel.start_consuming()
#     except KeyboardInterrupt:
#         print("Consumer stopped by user.")
#     finally:
#         connection.close()

# if __name__ == "__main__":
#     # Run the consumer in a separate thread to simulate concurrency
#     threading.Thread(target=start_consumer, daemon=True).start()
    
#     # Keep the main thread running
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print("Shutting down the consumer.")


import pika
import json
from datetime import datetime

# RabbitMQ configuration
RABBITMQ_HOST = "localhost"
EXCHANGE_NAME = "chat_exchange"

def callback(ch, method, properties, body):
    """Callback function to handle incoming messages."""
    message = json.loads(body)
    print(f"Received: {message}")
    
    # Process the message
    user_message = message.get("message", "").lower()
    if user_message == "hello":
        response = "Hi there! 😊"
    elif "weather" in user_message:
        response = "The weather is sunny and bright! ☀️"
    elif "joke" in user_message:
        response = "Why did the chicken cross the road? To get to the other side! 😂"
    elif "time" in user_message:
        response = "Sorry, I can't tell the exact time right now! ⏰"
    else:
        response = "I'm not sure how to respond to that. 🤔"

    response = {
            "from":"bot",
            "message": response, 
            "date":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    response_body = json.dumps(response)
    
    print(f"Response: {response_body}")

def main():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # Declare a fanout exchange
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="fanout")

    # Declare a queue with a unique name for this consumer and bind it to the exchange
    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name)

    print("Waiting for messages. To exit, press CTRL+C")

    # Consume messages from the queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    # Start consuming
    channel.start_consuming()

if __name__ == "__main__":
    main()
