from abuse import get_data
from urlscan import get_ip_address
import time
from models import IPAddressData
import asyncio
from rich import print

async def stream_data(url,user):
    import json
    from kafka import KafkaProducer

    producer = KafkaProducer(bootstrap_servers=['localhost:9092'], max_block_ms=5000)
    curr_time = time.time()

    hostname= await get_ip_address(url)
    # print(f"IP Address: {hostname}")
    res = await get_data(hostname)
    print(f"Data: {res}")
    # print(res)
    producer.send(user, json.dumps(res).encode('utf-8'))
    print(f"Data sent to {user} topic")


if __name__ == "__main__":
    url="gomovies.sx"
    user = "nj_created"

    res = asyncio.run(stream_data(url,user))
    # data = IPAddressData(**res)
    # data = stream_data(url,user)
    print(res)
    