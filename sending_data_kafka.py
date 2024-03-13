
import json
import time
from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError
import faker_data


# Create a Kafka topic
topic_name = "credit_card_transactions"
admin_client = KafkaAdminClient(bootstrap_servers="localhost:9092")

# Try to create the topic. If it already exists, catch the exception.
try:
    admin_client.create_topics(new_topics=[NewTopic(name=topic_name, num_partitions=1, replication_factor=1)])
    print(f"Topic {topic_name} created")
except TopicAlreadyExistsError:
    print(f"Topic {topic_name} already exists")

# Kafka Producer
producer = KafkaProducer(bootstrap_servers="localhost:9092")

# List to store transactions for comparison
generated_transactions = []
num_transactions =10
for _ in range(num_transactions):
    transaction = faker_data.generate_transaction()
    
    generated_transactions.append(transaction)
    
    transaction_message = json.dumps(transaction).encode("utf-8")
    
    producer.send("credit_card_transactions", transaction_message)
    
    producer.flush()
    
    time.sleep(1)  # Adjust interval as needed

print(f"Sent {num_transactions} transactions to Kafka.")
# # Kafka Producer
# producer = KafkaProducer(bootstrap_servers="localhost:9092")

# # Push a finite number of transactions to the topic
# num_transactions = 10  # Set the desired number of transactions
# for _ in range(num_transactions):
#     transaction = faker_data.generate_transaction()
#     print(f"Sending: {transaction}")  # Print the transaction for verification
#     producer.send(topic_name, json.dumps(transaction).encode("utf-8"))
#     producer.flush()
#     time.sleep(1)  # Adjust interval as needed

# print(f"Finished sending {num_transactions} transactions to topic {topic_name}.")
