import time
from threading import Lock

# Global variables
lock = Lock()
request_count = 0
max_requests = 10
response_times = []  # Track response times for all requests (both sequential and concurrent)
request_log = []  # Log to track request start and end times

# Increment request count with synchronization
def increment_request_count():
    global request_count
    with lock:
        request_count += 1
    return request_count

# Function to check if the simulation should stop (max requests reached)
def should_stop_simulation():
    global request_count
    return request_count > max_requests

# Record response time for each request
def record_response_time(start_time):
    end_time = time.time()
    response_times.append(end_time - start_time)

# Log the request start and end times
def log_request_start(request_id, start_time):
    global request_log
    with lock:
        request_log.append((request_id, start_time))

def log_request_end(request_id, end_time):
    global request_log
    with lock:
        # Update the request log with the end time
        for i, entry in enumerate(request_log):
            if len(entry) == 2:  # Ensure the entry only has two values (request_id and start_time)
                req_id, start = entry
                if req_id == request_id:
                    request_log[i] = (req_id, start, end_time)  # Add the end time to the log entry
                    break

# Calculate the average response time and print it
def calculate_avg_response_time():
    if len(response_times) > 0:
        avg_time = sum(response_times) / len(response_times)
        print(f"Average response time: {avg_time:.5f} seconds")

# Analyze the request log to determine if requests were sequential or concurrent
def analyze_request_log():
    print("\nAnalyzing Request Log for Concurrency...")
    for i, (request_id, start_time, end_time) in enumerate(request_log):
        if i > 0:
            prev_end_time = request_log[i - 1][2]  # Get previous request's end time
            if start_time < prev_end_time:
                print(f"REQUEST {request_id} was concurrent with the previous request.")
            else:
                print(f"REQUEST {request_id} was sequential after the previous request.")
