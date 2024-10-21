# utils/csv_logger.py

import csv
import datetime
import os

# Path to save the CSV file
csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results', 'response_times.csv')

# Initialize the CSV file with headers
def initialize_csv():
    """Create a new CSV file or overwrite the existing one, and write the headers."""
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Request Number', 'Product Searched', 'Response Time (s)', 'Mode'])

# Log request details into the CSV file
def log_to_csv(request_number, product_name, response_time, mode):
    """Append a row of request data to the CSV file."""
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([request_number, product_name, response_time, mode])

    
    # cretaing a text file also
    """Append a row of request data to a text file with timestamp."""
    txt_file_path = 'transactions_log.txt'
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")[:-3]
    
    with open(txt_file_path, mode='a') as file:
        file.write(f"{timestamp} - Request {request_number}: {request_number} bought {product_name} from {seller_id}\n")