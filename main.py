import argparse
import time
import threading
from services.peer_manager import initialize_peers
from services.buyer_behavior import buyer_behavior
from services.seller_behavior import switch_product

if __name__ == "__main__":
    # Command-line argument handling
    parser = argparse.ArgumentParser(description="P2P Buy-Sell Simulation")
    parser.add_argument("N", type=int, help="Number of peers in the network")
    args = parser.parse_args()

    N = args.N  # Get the value of N from the command-line argument

    # Initialize peers
    peers = initialize_peers(N)

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
    
    # Start buyer threads
    for buyer in buyer_peers:
        threading.Thread(target=buyer_behavior, args=(buyer, products)).start()

    time.sleep(5)

    # Handle product switch for sellers
    for seller in seller_peers:
        if seller.stock <= 0:
            switch_product(seller, products)