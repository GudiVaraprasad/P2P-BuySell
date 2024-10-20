import argparse
import time
import threading
from services.peer_manager import initialize_peers
from services.buyer_behavior import buyer_behavior
from services.seller_behavior import switch_product
from utils.csv_logger import initialize_csv

if __name__ == "__main__":
    # Command-line argument handling for N and mode (sequential or concurrent)
    parser = argparse.ArgumentParser(description="P2P Buy-Sell Simulation")
    parser.add_argument("N", type=int, help="Number of peers in the network")
    parser.add_argument("--mode", type=str, default="sequential", choices=['sequential', 'concurrent'],
                        help="Specify whether to run in sequential or concurrent mode")
    args = parser.parse_args()

    N = args.N  # Get the number of peers
    mode = args.mode  # Get the mode (sequential or concurrent)

    # Initialize CSV file for logging response times
    initialize_csv()  # Initialize CSV with headers

    # Initialize peers and calculate the graph diameter
    peers, graph_diameter = initialize_peers(N)

    # Start all peers
    for peer in peers:
        peer.start()

    # Verify that all peers have valid ports
    for peer in peers:
        assert peer.port is not None, f"Peer {peer.peer_id} does not have a valid port assigned!"
        print(f"Peer {peer.peer_id} is using port {peer.port} with role {peer.role}")

    buyer_peers = [peer for peer in peers if peer.role == 'buyer']
    seller_peers = [peer for peer in peers if peer.role == 'seller']
    
    products = ['fish', 'salt', 'boar']
    
    # Use the calculated graph diameter as the hop count for lookups
    for buyer in buyer_peers:
        threading.Thread(target=buyer_behavior, args=(buyer, products, graph_diameter, mode)).start()

    time.sleep(5)
    for seller in seller_peers:
        if seller.stock <= 0:
            switch_product(seller, products)