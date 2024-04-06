import os
import json

from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import JSONResponse
from typing import Dict

app = FastAPI()

# Test Endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# POST

# Prediction Endpoint
@app.get("/predict")
async def predict(request: Request):
    """
    This API endpoint is used to predict the safety of a list of URLs.
    :param request: Request object
    """
    # Get the data from the request
    data = await request.json()
    
    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="Data must be a dictionary")
    
    results = {}
    for url, flag in data.items():
        if not isinstance(flag, bool):
            raise HTTPException
        
        results[url] = "safe" if not flag else "unsafe"

    return results

# Root Endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}