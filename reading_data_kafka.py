import json
import pandas as pd
from kafka import KafkaConsumer
num_messages = 100
# Kafka Consumer
def consume_transactions_from_kafka(topic_name, bootstrap_servers="localhost:9092", num_messages = 100):

    consumer = KafkaConsumer(
        'credit_card_transactions',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',  # Start reading at the earliest message
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    # Initialize an empty list to store messages
    messages = []

    # Consume messages
    try:
        for message in consumer:
            messages.append(message.value)
            print(f"Received message: {message.value}")
            # Break after receiving a certain number of messages
            # Remove or adjust this limit based on your needs
            if len(messages) >= num_messages:
                break
    finally:
        consumer.close()
    
    df = pd.DataFrame(messages)
    print(df)

    df.to_csv('kafka_messages.csv', index=False)
    return messages
