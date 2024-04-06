from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
import requests

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

urls = ["goolge.com", "nj.sg", "twitter.com", "gomovies.sx", "ww4.gogoanime2.org", "readm.org"]
for url in urls:
    producer.send('urlsTopic', value={"url": url})
producer.flush()

consumer = KafkaConsumer(
    'urlsTopic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='url-consumers',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')))

fastapi_endpoint = "http://localhost:8000/scan-urls/"

for message in consumer:
    url_data = message.value
    print(f"Sending URL to FastAPI: {url_data['url']}")
    try:
        response = requests.post(fastapi_endpoint, json={"urls": [url_data['url']]})
        if response.status_code == 200:
            print(f"URL {url_data['url']} processed successfully.")
        else:
            print(f"Failed to process URL {url_data['url']}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")