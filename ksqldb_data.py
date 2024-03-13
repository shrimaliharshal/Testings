import json
import requests
from kafka import KafkaConsumer, KafkaProducer
import fraudulent

# ksqlDB server endpoint
ksql_url = 'http://localhost:8088/ksql'
# Headers for HTTP request
headers = {
    'Content-Type': 'application/vnd.ksql.v1+json; charset=utf-8',
}

# The SQL statement to create the stream, if it doesn't already exist
create_stream_sql = {
    "ksql": "CREATE STREAM IF NOT EXISTS TRANSACTIONS (CARD_NUMBER STRING, AMOUNT DOUBLE, LOCATION STRUCT<CITY STRING, STATE STRING>, TIMESTAMP STRING, MERCHANT_CATEGORY STRING, CURRENCY STRING, DEVICE_TYPE STRING) WITH (KAFKA_TOPIC='credit_card_transactions', KEY_FORMAT='KAFKA', VALUE_FORMAT='JSON');",
    "streamsProperties": {}
}

response = requests.post(ksql_url, headers=headers, data=json.dumps(create_stream_sql))
if response.status_code == 200:
    print("Stream creation attempted.")
    response_data = response.json()
    if response_data[0]['@type'] == 'currentStatus':
        print("Statement executed successfully or stream already exists.")
    elif response_data[0]['@type'] == 'statement_error':
        print(f"Error executing statement: {response_data[0]['message']}")
else:
    print("Failed to communicate with ksqlDB server.")


# Kafka consumer to read transactions
consumer = KafkaConsumer(
    'credit_card_transactions',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Kafka producer to publish flagged transactions
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)


for message in consumer:
    transaction = message.value
    if fraudulent.is_fraudulent(transaction):
        print(f"Flagged transaction: {transaction}")
        # Send to a different topic for flagged transactions
        producer.send('flagged_transactions', transaction)
        producer.flush()

# Remember to close the consumer and producer when done
consumer.close()
producer.close()
