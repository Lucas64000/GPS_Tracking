import os
import sys
import time


# Compatibility for Python 3.12+
if sys.version_info >= (3, 12, 0):
    import six
    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaProducer

# Get configuration from environment variables
topic = os.getenv('KAFKA_TOPIC', 'topic_test')
#bootstrap_server = os.getenv('KAFKA_SERVER', 'broker:9093')
bootstrap_server = 'broker:29092'

producer_id = os.getenv('PRODUCER_ID', 'unknown')

# Kafka producer setup
producer = KafkaProducer(bootstrap_servers=[bootstrap_server])

print(f"Producer {producer_id} started, sending messages to {topic}.")
# Send a message every 2 seconds
message_counter = 0
while True:
    message = f"Message {message_counter} from producer {producer_id}"
    producer.send(topic, message.encode('utf-8'))
    print(f"Sent: {message}")
    message_counter += 1
    time.sleep(2)
