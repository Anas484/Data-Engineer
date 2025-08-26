from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
from api import get_random_product
from time import sleep
import random


producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
 

def send_product():
    try:
        b = random.choice("abcdefghijklmnopqrstuvwxyz")
        c = "".join(random.choices("123456789", k=2))
        product = get_random_product()
        data = {
            "id": str(product["id"]) + b + c,
            "title": product["title"],
            "category":product["category"],
            "price": product["price"]
        }
        future = producer.send('products', value=data)
        record_metadata = future.get(timeout=10)
    except KafkaError as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    while True:
        send_product()
        sleep(1)

