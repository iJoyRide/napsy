from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

urls = ["goolge.com", "nj.sg", "twitter.com", "gomovies.sx", "ww4.gogoanime2.org", "readm.org"]
for url in urls:
    producer.send('urlsTopic', value={"url": url})
producer.flush()
