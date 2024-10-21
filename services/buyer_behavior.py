import random
import time
import threading
from protocol.message import Message
import json
from utils.response_time_logger import (increment_request_count, 
                                        should_stop_simulation, 
                                        record_response_time, 
                                        log_request_start, 
                                        log_request_end, 
                                        calculate_avg_response_time, 
                                        analyze_request_log)
from utils.csv_logger import initialize_csv, log_to_csv

# Global flag to signal termination
terminate_flag = False

# Path to save the CSV file (this file will have performance metrics for later analysis)
csv_file_path = 'response_times_log.csv'

def buyer_behavior(buyer_peer, products, hop_count, mode='sequential'):
    """Buyer continuously searches for products with random delays between searches."""
    while not terminate_flag:
        product_to_buy = random.choice(products)
        continue_search(buyer_peer, product_to_buy, hop_count)  # Pass the hop count dynamically
        
       # Sequential mode: Wait between requests
        if mode == 'sequential':
            wait_time = random.randint(1, 2)  # Wait for 1 to 2 seconds
            print(f"Buyer {buyer_peer.peer_id} will wait {wait_time} seconds before the next purchase.")
            # Check the termination flag during sleep
            for _ in range(wait_time):
                if terminate_flag:
                    analyze_request_log()  # Analyze requests after all requests are done
                    return  # Exit if termination flag is set
                time.sleep(1)
        
        # Concurrent mode: No wait between requests
        elif mode == 'concurrent':
            print(f"Buyer {buyer_peer.peer_id} is making concurrent requests.")  # No delay in concurrent mode
            # In concurrent mode, we still need to check for the termination flag periodically
            if terminate_flag:
                analyze_request_log()  # Analyze requests after all requests are done
                return  # Exit if termination flag is set

def continue_search(buyer_peer, product_name, max_hops=3, mode='sequential'):
    # Start time of the request
    start_time = time.time()

    # Increment request count and check if the simulation should stop
    current_request = increment_request_count()
    
    # If max_requests has been reached, stop further requests
    if should_stop_simulation():
        print(f"\nMax requests reached: {current_request-1}. Stopping simulation.")
        calculate_avg_response_time()  # Calculate and print the average response time
        global terminate_flag
        terminate_flag = True  # Signal all threads to stop
        return

    # Log the request start time
    log_request_start(current_request, start_time)
    
    # Display request count and separator lines
    print(f"\nREQUEST {current_request}")
    print("-" * 40)
    print(f"Buyer Peer {buyer_peer.peer_id} is looking for {product_name}")

    # Create lookup message
    lookup_message = Message.lookup(
        buyer_id=buyer_peer.peer_id, 
        product_name=product_name, 
        hop_count=max_hops
    )

    # Send the lookup message to neighbors
    for neighbor_ip, neighbor_port in buyer_peer.neighbors:  # Now neighbors contain (ip, port) tuples
        buyer_peer.send_message(neighbor_ip, neighbor_port, json.dumps(lookup_message))
    
    # Record response time for this request
    response_time = time.time() - start_time
    record_response_time(start_time)

    # Log the request end time
    end_time = time.time()
    log_request_end(current_request, end_time)  # Log the end of the request

    # Log the data into the CSV file
    log_to_csv(current_request, product_name, response_time, mode)

    # Print the communication summary
    print("-" * 50)