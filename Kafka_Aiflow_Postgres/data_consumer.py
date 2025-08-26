from kafka import KafkaConsumer
import json
import psycopg2
import time

def safe_json_deserializer(x):
    try:
        return json.loads(x.decode('utf-8'))
    except Exception as e:
        print(f"Invalid JSON received: {x} — Error: {e}")
        return None

def consume_and_store_products():
    consumer = KafkaConsumer(
        'products',
        bootstrap_servers=['kafka:9092'],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        value_deserializer=safe_json_deserializer
    )

    conn = psycopg2.connect(
        host="host.docker.internal",
        database="Products",
        user="postgres",
        password="hello"
    )
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO products (id, title, price, category)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """

    try:
        for message in consumer:
            data = message.value
            if data:
                try:
                    product_id = data.get("id")
                    title = data.get("title")
                    price = data.get("price")
                    category = data.get("category")

                    if None not in (product_id, title, price, category):
                        cursor.execute(insert_query, (product_id, title, price, category))
                        conn.commit()
                        print(f"Inserted: {product_id}, {title}, {price}, {category}")
                    else:
                        print(f"Incomplete data skipped: {data}")
                except Exception as e:
                    print(f"Error inserting data: {data} — Error: {e}")

    except KeyboardInterrupt:
        print("Stopping consumer...")

    finally:
        consumer.close()
        cursor.close()
        conn.close()


if __name__ == "__main__":
    while True:
        consume_and_store_products()
        time.sleep(1)