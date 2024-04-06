from abuse import get_data
from urlscan import get_ip_address
import time
from models import IPAddressData
import asyncio
from rich import print

def stream_data(url,user):
    import json
    from kafka import KafkaProducer

    producer = KafkaProducer(bootstrap_servers=['localhost:9092'], max_block_ms=5000)
    curr_time = time.time()



    hostname=asyncio.run( get_ip_address(url))
    res = asyncio.run(get_data(hostname))
    print(res)
    producer.send(user, json.dumps(res).encode('utf-8'))


if __name__ == "__main__":
    url="gomovies.sx"
    user = "nj_created"
    res = stream_data(url,user)
    # data = IPAddressData(**res)
    # data = stream_data(url,user)
    print(res)
    