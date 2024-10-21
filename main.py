import argparse
import time
import threading
import socket
from services.peer_manager import initialize_peers
from services.buyer_behavior import buyer_behavior
from services.seller_behavior import switch_product
from utils.csv_logger import initialize_csv
from network.peer_registry import initialize_registry, register_peer, wait_for_all_peers
from network.network_config import load_config

if __name__ == "__main__":
    # Command-line argument handling for N and mode (sequential or concurrent)
    parser = argparse.ArgumentParser(description="P2P Buy-Sell Simulation")
    parser.add_argument("N", type=int, help="Total number of peers in the network")
    args = parser.parse_args()

    # Load the configuration
    config = load_config()

    # Get total peers, mode, and system information from the config
    total_peers = args.N
    system_1_ip = config['system_1']['ip']
    system_2_ip = config['system_2']['ip']
    system_1_peers = config['system_1']['peers_count']
    system_2_peers = config['system_2']['peers_count']
    mode = config['mode']

    # Determine which system this is based on its IP address
    local_ip = socket.gethostbyname(socket.gethostname())

    # Assign the number of peers based on the local system
    if local_ip == system_1_ip:
        N = system_1_peers
        print(f"Running {N} peers on System 1 with IP {local_ip} in {mode} mode.")
    elif local_ip == system_2_ip:
        N = system_2_peers
        print(f"Running {N} peers on System 2 with IP {local_ip} in {mode} mode.")
    else:
        raise ValueError(f"Unknown system IP: {local_ip}")
    
    # Initialize the peer registry
    initialize_registry()

    # Register each peer as they start
    for peer_id in range(N):
        register_peer(peer_id, local_ip)

    # Wait for all peers (total_peers = N from command line)
    wait_for_all_peers(total_peers)

    # Initialize CSV file for logging response times
    initialize_csv()  # Initialize CSV with headers

    # Initialize peers and calculate the graph diameter
    peers, graph_diameter = initialize_peers(N, local_ip, known_system_ips=[system_1_ip, system_2_ip])

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