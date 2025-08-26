import json
import random
from datetime import datetime, timedelta
import time

first_names = ["John", "Peter", "Emma", "Sara", "Anas", "Liam"]
last_names = ["Smith", "Wiggins", "Khan", "Sharma", "Johnson"]

def generate_card(start_with=None):
    if start_with and random.random() < 0.8:
        card = str(start_with) + ''.join(str(random.randint(0, 9)) for _ in range(15))
    else:
        first_digit = random.choice([d for d in range(1, 10) if d != 4])
        card = str(first_digit) + ''.join(str(random.randint(0, 9)) for _ in range(15))
    return card

def format_card(card):
    return '-'.join([card[i:i+4] for i in range(0, 16, 4)])

def generate_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_expiry():
    if random.random() < 0.2 :
        past_date = datetime.now() - timedelta(days=random.randint(365, 5 * 365))
        return past_date.strftime("%m/%y")
    else:
        future_date = datetime.now() + timedelta(days=random.randint(365, 5 * 365))
        return future_date.strftime("%m/%y")  # MM/YY

def generate_cvv():
    return str(random.randint(100, 999))

def generate_amount():
    return str(round(random.uniform(100.5, 5000.5),2))

def generate_time():
    return str(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))

def generate_card_entry(start_with=4):
    raw_card = generate_card(start_with)
    return {
        "body":{
            "card_number": format_card(raw_card),
            "name": generate_name(),
            "expiry": generate_expiry(),
            "cvv": generate_cvv(),
            "amount" : generate_amount(),
            "timestamp" : generate_time()
            }
            }


def lambda_handler(event, context):
    card = generate_card_entry()["body"]
    return {
        'statusCode': 200,
        'body': json.dumps(card)
    }


