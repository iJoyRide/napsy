import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file


def get_ip_address(hostname):
    api_key = os.getenv("API_KEY")

    headers = {'API-Key': api_key ,'Content-Type':'application/json'}
    data = {"url": hostname, "visibility": "public"}
    response = requests.post('https://urlscan.io/api/v1/scan/',headers=headers, data=json.dumps(data))
    # print(response.text)
    # print(response.json())
    reply = response.json()
    scan_completed = False
    print("acessing report")
    while not scan_completed:
        try:
            res = requests.get(reply['api'])
            report  = res.json()
            message = report['message']

            if message != "Scan is not finished yet":
                scan_completed=True
        except Exception as e:
            break
    page_ip = report['page']['ip']
    return page_ip
