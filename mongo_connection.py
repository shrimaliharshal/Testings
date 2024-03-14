from pymongo import MongoClient
import pandas as pd
import json
from kafka import KafkaConsumer, KafkaProducer
import fraudulent
import ksqldb_data
# MongoDB connection setup


KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
MONGO_URI = 'mongodb://localhost:27017/'


def insert_flagged_transactions_into_mongo():
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client['fraud_detection']
    collection = db['flagged_transactions']
    consumer = KafkaConsumer('fraud_transactions', bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, auto_offset_reset='earliest', value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    fraud_count = 0
    for message in consumer:
        collection.insert_one(message.value)
        fraud_count += 1
        print(f"Inserted fraud transaction into MongoDB: {message.value}")
        
        
    print(f"Total fraudulent transactions inserted into MongoDB: {fraud_count}")
    consumer.close()
    mongo_client.close()