from kafka import KafkaConsumer
import json
from rich import print

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    'virustotalResultsTopic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',  # Start reading at the earliest message if this is a new consumer group
    group_id='virustotal-results-consumer',  # Consumer group ID
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # Deserialize messages from JSON
)

print("Listening for messages on 'virustotalResultsTopic'. Press Ctrl+C to stop.")

try:
    for message in consumer:
        message_value = message.value
        url = message_value.get('url')
        results = message_value.get('results')
        print(f"Received scan results for URL: {url}")
        print("Results:")
        for key, value in results.items():
            print(f"  {key}: {value}")
except KeyboardInterrupt:
    print("Stopped listening for messages.")
finally:
    consumer.close()

