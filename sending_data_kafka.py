
import json
import time
from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError
import faker_data


topic_name = "credit_card_transactions"

# Create a Kafka topic
def create_kafka_topic(topic_name, bootstrap_servers="localhost:9092"):

    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
    
    try:
        admin_client.create_topics(new_topics=[NewTopic(name=topic_name, num_partitions=1, replication_factor=1)])
        print(f"Topic {topic_name} created")
    except TopicAlreadyExistsError:
        print(f"Topic {topic_name} already exists")

# Sending data to Kafka
def send_transactions_to_kafka(num_transactions, topic_name, BOOTSTRAP_SERVERS="localhost:9092"):
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)

    # List to store transactions for comparison
    generated_transactions = []
    
    for _ in range(num_transactions):
        transaction = faker_data.generate_transaction()
        
        generated_transactions.append(transaction)
        
        transaction_message = json.dumps(transaction).encode("utf-8")
        
        producer.send(topic_name, transaction_message)
        
        producer.flush()
        
        time.sleep(1)  # Adjust interval as needed

    print(f"Sent {num_transactions} transactions to Kafka.")
