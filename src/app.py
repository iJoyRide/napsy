import os
import json
import re
from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import JSONResponse
from typing import Dict

app = FastAPI()

# POST
@app.post("/post")
async def post_website(request: Request):
    data = await request.json()

    ip_addresses = []
    for website in data["websites"]:
        # Extract ip address from website
        pattern = re.compile(r'^(https?://)?(www\.)?([a-zA-Z0-9-]+)\.([a-zA-Z]{2,})(/[a-zA-Z0-9-._/]*)*$')
        is_url =  bool(pattern.match(website))
        if is_url:
            ip_addresses.append(website)
        else:
            ip_addresses.append('0')

    return {"ip_addresses": ip_addresses}

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