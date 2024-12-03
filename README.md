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
Code: 1_send.py
## Message Consumer
- Listens to the queue and processes incoming messages.
- Provides chatbot-like responses based on messages map:
   "Hello" → "Hi there! 😊"
   "Tell me a joke" → "Why did the chicken cross the road? To get to the other side! 😂"
Code: 2_receive.py
