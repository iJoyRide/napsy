import os
import json
import time
import requests
from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import JSONResponse
from kafka import KafkaConsumer, KafkaProducer

app = FastAPI()

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# POST
@app.post("/post")
async def post_website(request: Request):
    # Kafka
    data = await request.json()

    ip_addresses = []
    for website in data["websites"]:
        producer.send('urlsTopic', value={"url": url})

    return {"websites": website}

# Post
@app.post("/predict")
async def predict(request: Request):
    data = await request.json()

    # If the data is not a dictionary, raise an error
    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="Data must be a dictionary")

    results = {}
    for url, unsafe_flag in data.items():
        if not isinstance(unsafe_flag, bool):
            raise HTTPException(status_code=400, detail=f"Invalid value for {url}. Expected a boolean.")
        results[url] = "safe" if not unsafe_flag else "unsafe"
    
    return results
