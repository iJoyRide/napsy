import requests
import json
import os
from dotenv import load_dotenv
import httpx
    # res = get_data(hostname)
# Load environment variables from .env file
load_dotenv()

async def get_ip_address(hostname):
    # print(hostname)
    api_key = os.getenv("API_KEY")

    headers = {'API-Key': api_key ,'Content-Type':'application/json'}
    data = {"url": hostname, "visibility": "public"}
    async with httpx.AsyncClient() as client:
        response = await client.post('https://urlscan.io/api/v1/scan/', headers=headers, data=json.dumps(data))
    
    reply = response.json()
    print(reply)
    scan_completed = False
    print("acessing report")
    while not scan_completed:
        try:
            res = httpx.get(reply['api'])
            report  = res.json()
            message = report['message']

            if message != "Scan is not finished yet":
                scan_completed=True
            page_ip = report['page']['ip']
            print(page_ip)
            return page_ip
        except Exception as e:
            break


