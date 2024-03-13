import faker
import json
import time
from kafka import KafkaProducer

fake = faker.Faker()

def generate_transaction():
    return {
        "card_number": fake.credit_card_number(),
        "amount": str(fake.pydecimal(positive=True, min_value=1, max_value=1000, right_digits=2)),
        "timestamp": fake.date_time().isoformat(),
        "location": {
            "city": fake.city(),
            "state": fake.state_abbr()
        },
        "merchant_category": fake.random_element(elements=('Grocery', 'Electronics', 'Clothing', 'Entertainment', 'Utilities')),
        "currency": fake.currency_code(),  # Adding currency field
        "device_type": fake.random_element(elements=('Mobile', 'Desktop', 'Tablet'))  # Adding device type field
    }

# Number of transactions to generate and send 
num_transactions = 10  # Adjust as needed

# # Kafka Producer
# producer = KafkaProducer(bootstrap_servers="localhost:9092")

# # List to store transactions for comparison
# generated_transactions = []

# for _ in range(num_transactions):
#     transaction = generate_transaction()
    
#     generated_transactions.append(transaction)
    
#     transaction_message = json.dumps(transaction).encode("utf-8")
    
#     producer.send("credit_card_transactions", transaction_message)
    
#     producer.flush()
    
#     time.sleep(1)  # Adjust interval as needed

# print(f"Sent {num_transactions} transactions to Kafka.")