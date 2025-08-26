from dotenv import load_dotenv
import os
from supabase import create_client
import random
import time
from datetime import datetime
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json



load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)


consumer = KafkaConsumer(
    'sensor',  
    bootstrap_servers='localhost:9092', 
    auto_offset_reset='latest',        
    enable_auto_commit=True,             
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    data = message.value
    try:
        response = supabase.table("sensor").insert({
            "sensor_id": data.get("sensor_id"),
            "temperature": data.get("temperature"),
            "humidity": data.get("humidity"),
            "vibration": data.get("vibration"),
            "timestamp": data.get("timestamp")
        }).execute()
        print("Inserted:", response.data)
    except Exception as e:
        print("Insert failed:", e)

