from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
from kafka import KafkaProducer, KafkaConsumer
import json
from threading import Thread
from virus import check_virustotal
from rich import print

app = FastAPI()

class UrlList(BaseModel):
    urls: List[str]

# Configure Kafka Producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

def kafka_consumer():
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

# Start Kafka consumer in a separate thread
consumer_thread = Thread(target=kafka_consumer)
consumer_thread.daemon = True  # Ensure the thread terminates when the main application exits
consumer_thread.start()

@app.post("/scan-urls/")
async def scan_urls(url_list: UrlList):
    api_key = os.getenv("APPI_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key is not configured correctly.")
    
    for url in url_list.urls:
        results = check_virustotal(url, api_key)
        # Assuming 'results' is a dictionary returned from 'check_virustotal'
        if results:
            producer.send('virustotalResultsTopic', value={"url": url, "results": results})
            producer.flush()  # Flush the producer after each message to ensure it's sent immediately
    
    return {"message": "URLs are being scanned and results will be sent to Kafka."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


