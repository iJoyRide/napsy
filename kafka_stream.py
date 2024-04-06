from abuse import get_data
from urlscan import get_ip_address
import time


def stream_data(url,user):
    import json
    from kafka import KafkaProducer

    producer = KafkaProducer(bootstrap_servers=['localhost:9092'], max_block_ms=5000)
    curr_time = time.time()



    hostname= get_ip_address(url)
    res = get_data(hostname)
    print(res)
    producer.send(user, json.dumps(res).encode('utf-8'))




url="gomovies.sx"
user = "nj_created"

# url="google.com"
# user = "google_created"
stream_data(url,user)