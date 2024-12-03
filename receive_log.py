import pika
import threading
import json
import logging
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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[
        logging.FileHandler("chatbot.log"),
        logging.StreamHandler()
    ]
)

def process_message(body):
    """
    Process an incoming message and respond.
    """
    try:
        # Decode the JSON message
        data = json.loads(body.decode("utf-8"))
        user_message = data.get("message", "")  # Extract the 'message' field

        # Log the received message
        logging.info(f"Received: {data}")

        # Get the response based on the RESPONSES map
        response_text = RESPONSES.get(user_message, "Sorry, I'm not sure how to respond to that. 🤔")

        # Create the response object
        response = {
            "from": "bot",
            "message": response_text,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # Log the response
        logging.info(f"Responded: {response}")

    except json.JSONDecodeError:
        logging.error("Error: Failed to decode the message! Message body: %s", body.decode("utf-8"))
    except Exception as e:
        logging.error("Unexpected error occurred: %s", str(e))

def callback(channel, method, properties, body):
    """
    RabbitMQ callback function to process messages.
    """
    try:
        threading.Thread(target=process_message, args=(body,)).start()
        # Acknowledge the message
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error("Failed to process the message: %s", str(e))

def main():
    """
    Main function to start the RabbitMQ consumer.
    """
    try:
        # Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()

        # Declare a temporary queue to bind to the exchange
        result = channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue

        # Bind the queue to the exchange
        channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name)

        logging.info("Chatbot is ready and listening for messages...")
        channel.basic_consume(queue=queue_name, on_message_callback=callback)

        channel.start_consuming()
    except KeyboardInterrupt:
        logging.info("Stopping the chatbot...")
    except Exception as e:
        logging.error("Failed to start the chatbot: %s", str(e))
    finally:
        try:
            connection.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
