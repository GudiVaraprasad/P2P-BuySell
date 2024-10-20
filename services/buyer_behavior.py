import random
import time
import threading
from protocol.message import Message
import json

# Global counters and synchronization mechanisms
lock = threading.Lock()
request_count = 0
max_requests = 1000
response_times = []

def continue_search(buyer_peer, product_name, max_hops=3):
    global request_count, response_times
    start_time = time.time()

    print(f"Buyer Peer {buyer_peer.peer_id} is looking for {product_name}")
    lookup_message = Message.lookup(
        buyer_id=buyer_peer.peer_id, 
        product_name=product_name, 
        hop_count=max_hops
    )
    
    with lock:
        if request_count >= max_requests:
            return  # Stop making new requests once max_requests is reached
        request_count += 1

    for neighbor_port in buyer_peer.neighbors:
        buyer_peer.send_message(neighbor_port, json.dumps(lookup_message))

    end_time = time.time()
    response_times.append(end_time - start_time)

    if request_count >= max_requests:
        print(f"Max requests reached: {request_count}. Stopping simulation.")
        print(f"Average response time: {sum(response_times) / len(response_times):.5f} seconds")
        exit(0)  # Terminate the program after max requests

def buyer_behavior(buyer_peer, products):
    """Buyer continuously searches for products with random delays between searches."""
    while True:
        product_to_buy = random.choice(products)
        continue_search(buyer_peer, product_to_buy)
        
        # Wait for a random amount of time before the next search
        wait_time = random.randint(5, 7)
        print(f"Buyer {buyer_peer.peer_id} will wait {wait_time} seconds before the next purchase.")
        time.sleep(wait_time)