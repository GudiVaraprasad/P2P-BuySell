# calculate_time.py
import threading
import time

# Global counters and synchronization mechanisms
lock = threading.Lock()
request_count = 0
max_requests = 10
response_times = []

# Function to calculate and print average response time
def record_response_time(start_time):
    end_time = time.time()
    response_time = end_time - start_time
    
    with lock:
        response_times.append(response_time)
    
def calculate_avg_response_time():
    """Calculate and print average response time when max requests are reached."""
    with lock:
        if len(response_times) > 0:
            avg_time = sum(response_times) / len(response_times)
            print(f"Average response time: {avg_time:.5f} seconds")
        else:
            print("No requests to process.")
    
def increment_request_count():
    global request_count
    with lock:
        request_count += 1
        return request_count

def should_stop_simulation():
    global request_count
    with lock:
        return request_count >= max_requests