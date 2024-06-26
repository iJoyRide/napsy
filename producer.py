from kafka import KafkaConsumer, KafkaProducer
import json
import requests
import time
from rich import print
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

class UrlsPayload(BaseModel):
    urls: list[str]

@app.post("/your-endpoint/")
async def send_urls(payload: UrlsPayload):
    for url in payload.urls:
        producer.send('urlsTopic', value={"url": url})
    producer.flush()
    return {"message": "URLs sent to Kafka successfully."}


# Consumer Configuration
consumer = KafkaConsumer(
    'urlsTopic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='url-consumers',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')))

fastapi_endpoint = "http://localhost:8000/scan-urls/"

# Initial sleep time based on the known rate limit (e.g., 4 URLs per 1 minute)
sleep_time = 60 / 4  # 15 secs

for message in consumer:
    url_data = message.value
    print(f"Sending URL to FastAPI: {url_data['url']}")

    try:
        response = requests.post(fastapi_endpoint, json={"urls": [url_data['url']]})

        if response.status_code == 200:
            print(f"URL {url_data['url']} processed successfully.")
            time.sleep(sleep_time)  # Sleep to respect the rate limit

        elif response.status_code == 429:  # Too Many Requests
            retry_after = int(response.headers.get("Retry-After", 60))  # Use the Retry-After header if available
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)  # Adjust sleeping time based on the Retry-After header

        else:
            print(f"Failed to process URL {url_data['url']}. Status code: {response.status_code}")
            # Handle other HTTP errors (e.g., server errors) appropriately

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        # Consider adding a delay here before retrying or moving on to the next URL
