
import json
import time
from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError
import faker_data

fake = faker_data.Faker()

def generate_transaction():
    return {
        "card_number": fake.credit_card_number(),
        "amount": fake.pydecimal(positive=True, min_value=1, max_value=1000, right_digits=2),
        "timestamp": fake.date_time(),
        "location": {
            "city": fake.city(),
            "state": fake.state_abbr()
        },
        "merchant_category": fake.random_element(elements=('Grocery', 'Electronics', 'Clothing', 'Entertainment', 'Utilities')),
        "currency": fake.currency_code(),
        "device_type": fake.random_element(elements=('Mobile', 'Desktop', 'Tablet'))
    }
