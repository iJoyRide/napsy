import requests
import json
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Defining the api-endpoint
url = 'https://api.abuseipdb.com/api/v2/check'

api_key = os.getenv("ABUSEAPI")

querystring = {
    'ipAddress': '118.25.6.39',
    'maxAgeInDays': '90'
}

headers = {
    'Accept': 'application/json',
    'Key': api_key 
}

response = requests.request(method='GET', url=url, headers=headers, params=querystring)

# Formatted output
decodedResponse = json.loads(response.text)
print(json.dumps(decodedResponse, sort_keys=True, indent=4))

