#!/opt/venv/bin/python
"""
Run this script to produce weather data to the Kafka topic.
./produce_weather_data.py

To stop it, press Ctrl+C.
"""

import json
import random
import socket
from time import sleep

import arrow
from confluent_kafka import KafkaError, KafkaException, Producer
from confluent_kafka.admin import AdminClient, NewTopic

# Data settings
START_DATETIME = arrow.get(2024, 11, 1, 0)
SLEEP_SEC = 0.5
DUPLICATE_CHANCE = 0.1
INPUT_DATA = [
    {"country": "Poland", "city": "Warsaw", "temperature": 20, "range": 5},
    {"country": "Poland", "city": "Krakow", "temperature": 22, "range": 4},
    {"country": "France", "city": "Paris", "temperature": 18, "range": 6},
    {"country": "France", "city": "Marseille", "temperature": 26, "range": 3},
    {"country": "USA", "city": "Miami", "temperature": 35, "range": 10},
    {"country": "USA", "city": "Los Angeles", "temperature": 30, "range": 5},
]

# Kafka settings
BOOTSTRAP_SERVERS = "kafka0:9092"
TOPIC_NAME = "weather-data"
TOPIC_NUM_PARTITIONS = 2

admin_client = AdminClient({
    "bootstrap.servers": BOOTSTRAP_SERVERS,
})

topic_config = {
    "num_partitions": TOPIC_NUM_PARTITIONS,
    "replication_factor": 1,
    "config": {
        "cleanup.policy": "delete",
        "compression.type": "gzip",
        "segment.ms": 60000 * 1,
        "retention.ms": 60000 * 2,
        "delete.retention.ms": 60000 * 1,
        "file.delete.delay.ms": 60000 * 1,
    },
}

new_topic = NewTopic(TOPIC_NAME, **topic_config)
fs = admin_client.create_topics([new_topic])
try:
    for f in fs.values():
        f.result()  # The result itself is None
except KafkaException as err:
    error = err.args[0]
    if error.code() != KafkaError.TOPIC_ALREADY_EXISTS:
        raise
    else:
        print(f"{TOPIC_NAME} topic already exists")
else:
    print(f"{TOPIC_NAME} topic created successfully")

producer_config = {
    "bootstrap.servers": BOOTSTRAP_SERVERS,
    "client.id": socket.gethostname(),
}
producer = Producer(producer_config)

measure_dt = START_DATETIME
messages_count = 0
try:
    while True:
        for data in INPUT_DATA:
            record = {
                "country": data["country"],
                "city": data["city"],
                "temperature": round(
                    random.uniform(
                        data["temperature"] - data["range"],
                        data["temperature"] + data["range"],
                    ),
                    1,
                ),
                "timestamp": measure_dt.isoformat(),
            }
            val = json.dumps(record)
            producer.produce(TOPIC_NAME, value=val)
            messages_count += 1
            print(record)
            if random.random() < DUPLICATE_CHANCE:
                sleep(0.1)
                producer.produce(TOPIC_NAME, value=val)
                messages_count += 1
                print(record)
        measure_dt = measure_dt.shift(minutes=1)
        print("-" * 105)
        sleep(SLEEP_SEC)
except KeyboardInterrupt:
    print("\nData production stopped.")
    producer.flush()
    print("Producer flushed.")
    print(f"Produced {messages_count} messages.")
