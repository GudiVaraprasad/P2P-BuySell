# utils/csv_logger.py

import csv
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
