"""
spark-submit --deploy-mode client --master local[*] examples/kafka_spark_streaming/kafka_producer.py
spark-submit --deploy-mode client --master spark://spark:7077 examples/kafka_spark_streaming/kafka_producer.py
"""

import json
import socket

from confluent_kafka import KafkaError, KafkaException, Producer
from confluent_kafka.admin import AdminClient, NewTopic
from faker import Faker

BOOTSTRAP_SERVERS = "kafka0:9092"
TOPIC_NAME = "streaming-sink"
TOPIC_NUM_PARTITIONS = 2

fake = Faker()

admin_client = AdminClient({
    "bootstrap.servers": BOOTSTRAP_SERVERS,
})

topic_config = {
    "num_partitions": TOPIC_NUM_PARTITIONS,
    "replication_factor": 1,
    "config": {
        "cleanup.policy": "delete",
        "compression.type": "gzip",
        "segment.ms": 60000,
        "retention.ms": 60000,
        "delete.retention.ms": 60000,
        "file.delete.delay.ms": 60000,
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

for i in range(10):
    record = {
        "id": i + 1,
        "country": fake.country(),
        "cities": [fake.city() for _ in range(3)],
    }
    print(record)
    val = json.dumps(record)
    producer.produce(TOPIC_NAME, value=val)

producer.flush()
