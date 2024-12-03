# python-rabbitmq

# RabbitMQ Message Producer

This project is a Python-based RabbitMQ message producer that demonstrates sending random chat messages to a fanout exchange. It generates messages with a simulated user and a timestamp, simulating high-traffic scenarios.

## Features

- Connects to RabbitMQ using the `pika` library.
- Publishes random messages to a fanout exchange (`chat_exchange`).
- Simulates high-traffic by sending messages every 0.5 seconds.

---

## Prerequisites

### 1. Install Python
Make sure Python 3.x is installed on your system. [Download Python](https://www.python.org/).

### 2. Install Dependencies
Install the required Python library:
```bash
pip install pika
