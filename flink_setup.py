from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

# Initialize StreamExecutionEnvironment and StreamTableEnvironment
env = StreamExecutionEnvironment.get_execution_environment()
env_settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
table_env = StreamTableEnvironment.create(env, environment_settings=env_settings)

# Assuming the table creation code is here
table_env.execute_sql("""
    CREATE TABLE flagged_transactions (
        card_number STRING,
        amount DOUBLE,
        location ROW<city STRING, state STRING>,
        transaction_time TIMESTAMP(3) METADATA FROM 'timestamp',  -- Assuming 'timestamp' is a field in your Kafka message representing the event time
        merchant_category STRING,
        currency STRING,
        device_type STRING
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'FLAGGED_TRANSACTION',
        'properties.bootstrap.servers' = 'localhost:9092',
        'scan.startup.mode' = 'earliest',
        'format' = 'json'
    )
""")

# Perform real-time analytics using SQL query
result = table_env.execute_sql("""
    SELECT
        TUMBLE_START(transaction_time, INTERVAL '1' MINUTE) AS window_start,
        COUNT(*) AS transaction_count,
        AVG(amount) AS avg_amount,
        SUM(amount) AS total_amount,
        MIN(amount) AS min_amount,
        MAX(amount) AS max_amount,
        merchant_category,
        currency,
        device_type
    FROM flagged_transactions
    GROUP BY 
        TUMBLE(transaction_time, INTERVAL '1' MINUTE),
        merchant_category,
        currency,
        device_type
""")

# Fetch and print the result for demonstration. In production, you might want to send this to a sink instead.
result.print()

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

# Initialize StreamExecutionEnvironment and StreamTableEnvironment
env = StreamExecutionEnvironment.get_execution_environment()
env_settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
table_env = StreamTableEnvironment.create(env, environment_settings=env_settings)

# Ensure that 'flagged_transactions' table is created and properly set up
# This step is crucial and must be done before executing the following queries

# Execute a simple query to count transactions
result = table_env.execute_sql("""
    SELECT COUNT(*) AS transaction_count
    FROM flagged_transactions
""")

# Fetch the result
with result.collect() as results:
    for row in results:
        print(row)
