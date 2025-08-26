import random
import time
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json

def generate_data():
    data = {
        'sensor_id': 20,
        'temperature': round(random.uniform(20.0,30.0),4),
        'humidity': round(random.uniform(30.0,50.0),4),
        'vibration': round(random.uniform(0.0,5.0),4),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    print(data)
    return data


producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def send_prod():
    try:
        sensor = generate_data()
        future = producer.send('sensor',value=sensor)
        metadata = future.get(timeout = 10)

    except KafkaError as e:
        print(f"Error sending message: {e}")     




if __name__ == '__main__':
    while True:
        send_prod()
        time.sleep(10)