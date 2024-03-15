from datetime import datetime, timedelta

# Example global variable to track the last transaction timestamp per card
last_transaction_time = {}

def is_fraudulent(transaction):
    # Convert amount to float for comparison
    amount = float(transaction['amount'])
    
    # Example thresholds and suspicious criteria
    high_amount_threshold = 500
    suspicious_categories = ['Electronics', 'Entertainment']
    rare_device_types = ['Tablet']
    
    # Check for high transaction amount
    if amount > high_amount_threshold:
        print("High amount detected.")
        return True
    
    # Check for transactions in suspicious categories
    if transaction['merchant_category'] in suspicious_categories:
        print("Suspicious category detected.")
        return True
    
    # Check for transactions from rare device types
    if transaction['device_type'] in rare_device_types:
        print("Rare device type detected.")
        return True
    
    # Check for frequent transactions in a short time
    card_number = transaction['card_number']
    current_time = datetime.fromisoformat(transaction['timestamp'])
    if card_number in last_transaction_time:
        # Assuming a threshold of 5 minutes for frequent transactions
        if current_time - last_transaction_time[card_number] < timedelta(minutes=5):
            print("Frequent transactions detected.")
            return True
    last_transaction_time[card_number] = current_time
    
    return False
