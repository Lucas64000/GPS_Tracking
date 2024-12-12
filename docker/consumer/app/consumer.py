
import sys

import time


# Compatibility for Python 3.12+
if sys.version_info >= (3, 12, 0):
    import six
    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaConsumer

# Kafka consumer setup
consumer = KafkaConsumer(
    'topic_test',
    bootstrap_servers=['broker:9093'],
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

print("Consumer started, waiting for messages...")
# Consume messages indefinitely
for message in consumer:
    print(f"Received: {message.value.decode('utf-8')}")
