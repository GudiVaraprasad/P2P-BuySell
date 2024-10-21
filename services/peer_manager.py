import random
import time
import threading
import networkx as nx  # Import NetworkX
import matplotlib.pyplot as plt  # Import Matplotlib for plotting
from network.peer import Peer
from utils.graph_algorithms import calculate_graph_diameter  # Import graph diameter calculation
from utils.visualize_network import visualize_network

def initialize_peers(N, local_ip, known_system_ips):
    roles = ['fish_seller', 'salt_seller', 'boar_seller', 'buyer']
    peer_roles = []
    has_buyer = False
    has_seller = False

    for i in range(N):
        if not has_buyer:
            peer_roles.append('buyer')
            has_buyer = True
        elif not has_seller:
            seller_type = random.choice(roles[:-1])
            peer_roles.append(seller_type)
            has_seller = True
        else:
            peer_roles.append(random.choice(roles))

    random.shuffle(peer_roles)
    peers = []

    # Dynamically assign ports and IPs to peers (dynamic port allocation)
    for peer_id, role in enumerate(peer_roles):
        ip = local_ip  # We will use the provided IP address
        if 'seller' in role:
            product_name = role.split('_')[0]  # Extract product name from role (e.g., fish, salt, boar)
            stock = random.randint(2, 5)
            # Dynamic port assignment happens when peer starts listening
            peers.append(Peer(peer_id=peer_id, role="seller", neighbors=[], product_name=product_name, stock=stock, ip=ip))
        else:
            peers.append(Peer(peer_id=peer_id, role="buyer", ip=ip, neighbors=[]))

    # Start listening for requests and dynamically assign ports to peers
    for peer in peers:
        threading.Thread(target=peer.listen_for_requests).start()

    peer_ports = {peer.peer_id: None for peer in peers}

    # Wait for ports to be dynamically assigned
    while None in peer_ports.values():
        for peer in peers:
            if peer.port is not None:
                peer_ports[peer.peer_id] = peer.port
        time.sleep(1)

    # Enforce ring topology or other topology, including known peers (cross-system)
    for i, peer in enumerate(peers):
        # Assign local neighbors as (ip, port) tuples
        peer.neighbors.extend([
            (local_ip, peer_ports[(i - 1) % N]),  # Connect to the previous peer in the ring
            (local_ip, peer_ports[(i + 1) % N]),  # Connect to the next peer in the ring
        ])
        peer.port_mapping = peer_ports  # Ensure port mapping is assigned here

    # Add cross-system peers as neighbors with IP and port
    for peer in peers:
        for system_ip in known_system_ips:
            if system_ip != local_ip:
                # Randomly pick two peers from the other system and connect them by IP and port
                cross_system_peer_id = random.choice(list(peer_ports.keys()))  # Choose a random peer from the other system
                cross_system_peer_port = peer_ports[cross_system_peer_id]
                peer.neighbors.append((system_ip, cross_system_peer_port))  # Add as (IP, port) tuple

    # Display the network structure visually using NetworkX
    visualize_network(peers)

    # After initializing peers, calculate graph diameter
    # graph_diameter = 3
    graph_diameter = calculate_graph_diameter(peers)
    print(f"Calculated graph diameter: {graph_diameter}")
    
    return peers, graph_diameter