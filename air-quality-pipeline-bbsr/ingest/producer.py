
import json
import time
from kafka import KafkaProducer
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'aq_bbsr'

def generate_fake_aq_data():
    return {
        "station_id": "bb_air_" + str(random.randint(1, 10)),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "pm25": round(random.uniform(10, 150), 2),
        "coordinates": [85.8245 + random.uniform(-0.01, 0.01), 20.2961 + random.uniform(-0.01, 0.01)]
    }

if __name__ == "__main__":
    print("Starting Kafka producer for air quality data...")
    while True:
        data = generate_fake_aq_data()
        producer.send(topic, value=data)
        print(f"Sent: {data}")
        time.sleep(2)  # every 2 seconds
