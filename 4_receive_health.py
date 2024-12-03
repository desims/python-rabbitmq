import pika
import json
from datetime import datetime
import logging
from flask import Flask, jsonify
import time
from concurrent.futures import ThreadPoolExecutor
import threading

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("consumer.log"),
        logging.StreamHandler()
    ]
)

# Flask app for health checks
app = Flask(__name__)

# RabbitMQ configuration
RABBITMQ_HOST = "localhost"
EXCHANGE_NAME = "chat_exchange"

# Global flags for service health
service_health = {"rabbitmq_connected": False, "processing": True}
service_health_lock = threading.Lock()

# Message response map
RESPONSES = {
    "Hello": "Hi there! 😊",
    "Tell me about weather": "The weather is sunny and bright! ☀️",
    "Tell me a joke": "Why did the chicken cross the road? To get to the other side! 😂",
    "What's the time?": "Sorry, I can't tell the exact time right now! ⏰"
}

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
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.submit(process_message, body)
        # Acknowledge the message
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error("Failed to process the message: %s", str(e))

def consume_messages():
    """
    Start the RabbitMQ consumer in a loop for reliability.
    """
    while True:
        try:
            # Connect to RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            channel = connection.channel()

            # Declare a temporary queue to bind to the exchange
            result = channel.queue_declare(queue="", exclusive=True)
            queue_name = result.method.queue

            # Bind the queue to the exchange
            channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name)

            with service_health_lock:
                service_health["rabbitmq_connected"] = True

            logging.info("Chatbot is ready and listening for messages...")
            channel.basic_consume(queue=queue_name, on_message_callback=callback)

            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            logging.critical(f"RabbitMQ connection error: {e}")
            with service_health_lock:
                service_health["rabbitmq_connected"] = False
            time.sleep(5)  # Retry connection
        except KeyboardInterrupt:
            logging.info("Consumer stopped by user.")
            with service_health_lock:
                service_health["processing"] = False
            break

# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    with service_health_lock:
        return jsonify({
            "status": "ok" if service_health["rabbitmq_connected"] and service_health["processing"] else "degraded",
            "details": service_health
        })

if __name__ == "__main__":
    # Run Flask app for health checks in a separate thread
    flask_thread = threading.Thread(target=app.run, kwargs={"port": 8080, "use_reloader": False})
    flask_thread.daemon = True
    flask_thread.start()

    # Start the RabbitMQ consumer
    consume_messages()
