import requests
import json
import os
from dotenv import load_dotenv
import asyncio
import httpx
# Load environment variables from .env file
load_dotenv()


async def get_data(hostname):
    url = 'https://api.abuseipdb.com/api/v2/check'

    api_key = os.getenv("ABUSEAPI")
    querystring = {
        # 'ipAddress': '118.25.6.39',
        'ipAddress': hostname,
        'maxAgeInDays': '90'
    }

    headers = {
        'Accept': 'application/json',
        'Key': api_key 
    }

    async with httpx.AsyncClient() as client:
        response = await client.request(method='GET', url=url, headers=headers, params=querystring)

    # Formatted output
    decodedResponse = json.loads(response.text)
    return decodedResponse