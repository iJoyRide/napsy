import os
import json

from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# POST

# GET
@app.get("/")
async def root():
    return {"message": "Hello World"}