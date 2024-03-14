import sending_data_kafka
import ksqldb_data
import mongo_connection
# Constants
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
KSQL_URL = 'http://localhost:8088/ksql'
HEADERS = {'Content-Type': 'application/vnd.ksql.v1+json; charset=utf-8'}
MONGO_URI = 'mongodb://localhost:27017/'
num_transactions = 50
topic_name = 'credit_card_transactions'
sending_data_kafka.create_kafka_topic(topic_name, KAFKA_BOOTSTRAP_SERVERS)
sending_data_kafka.send_transactions_to_kafka(num_transactions, topic_name, KAFKA_BOOTSTRAP_SERVERS)
ksqldb_data.setup_ksql()
mongo_connection.insert_flagged_transactions_into_mongo()
