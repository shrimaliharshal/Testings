from pymongo import MongoClient
import pandas as pd
import json
from kafka import KafkaConsumer, KafkaProducer
import fraudulent
import ksqldb_data
# MongoDB connection setup
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['fraud_detection']
collection = db['flagged_transactions']

# Continue with your Kafka consumer setup...

for message in ksqldb_data.consumer:
    transaction = message.value
    if fraudulent.is_fraudulent(transaction):
        print(f"Flagged transaction: {transaction}")
        # Insert into MongoDB
        collection.insert_one(transaction)

# Kafka producer part remains unchanged...

# To read data from MongoDB into a Pandas DataFrame
def read_data_to_dataframe():
    query = {}  # Adjust this query based on your needs
    cursor = collection.find(query)
    df = pd.DataFrame(list(cursor))
    return df

# Use this function to fetch and print the DataFrame
df = read_data_to_dataframe()
print(df.shape)
df.to_csv("fradulent_data.csv", index=False)
# Don't forget to close your MongoDB client, Kafka consumer, and producer when done
mongo_client.close()
ksqldb_data.consumer.close()
ksqldb_data.producer.close()
