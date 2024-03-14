import json
import requests
from kafka import KafkaConsumer, KafkaProducer


# ksqlDB server endpoint
ksql_url = 'http://localhost:8088/ksql'
# Headers for HTTP request
headers = {
    'Content-Type': 'application/vnd.ksql.v1+json; charset=utf-8',
}




# Function to execute SQL commands on ksqlDB server
def execute_ksql_command(ksql_url, headers, sql_command):
    response = requests.post(ksql_url, headers=headers, data=json.dumps(sql_command))
    if response.status_code == 200:
        print("SQL command executed successfully.")
    else:
        print("Failed to execute SQL command.")
        print(response.text)


def setup_ksql():
    # Execute SQL commands to create stream, function, and flagged transactions
    create_stream_sql = {
        "ksql": """CREATE STREAM IF NOT EXISTS TRANSACTIONS (
            CARD_NUMBER VARCHAR,
            AMOUNT DOUBLE,
            LOCATION STRUCT<CITY VARCHAR, STATE VARCHAR>,
            TIMESTAMP VARCHAR,
            MERCHANT_CATEGORY VARCHAR,
            CURRENCY VARCHAR,
            DEVICE_TYPE VARCHAR
        ) WITH (KAFKA_TOPIC='credit_card_transactions', VALUE_FORMAT='JSON');"""
    }
    # Define SQL command to create the flagged transactions stream
    create_flagged_transactions_sql = {
        "ksql": """CREATE STREAM FLAGGED_TRANSACTIONS AS
        SELECT * FROM TRANSACTIONS
        WHERE AMOUNT > 500
        OR MERCHANT_CATEGORY IN ('Electronics', 'Entertainment')
        OR DEVICE_TYPE = 'Tablet';"""
    }
    execute_ksql_command(ksql_url, headers, create_stream_sql)
    print("Starting ksqlDB setup...")
    execute_ksql_command(ksql_url, headers, create_flagged_transactions_sql)
    print("ksqlDB setup completed.")


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

