# main.py
from network.peer import Peer
from protocol.message import Message
import json 
import threading
import time
import random

def initialize_peers(N):
    roles = ["buyer", "seller"]
    products = ["fish", "salt", "boar"]

    peers = []
    
    # Randomly assign roles and products
    for peer_id in range(N):
        role = random.choice(roles)
        product = None if role == "buyer" else random.choice(products)
        stock = 10 if role == "seller" else 0
        peer = Peer(peer_id=peer_id, role=role, neighbors=[], product_name=product, stock=stock)
        peers.append(peer)

    # Start listening for each peer in a separate thread
    for peer in peers:
        threading.Thread(target=peer.listen_for_requests).start()

    # Dynamically assign neighbors based on assigned ports
    peer_ports = {peer.peer_id: None for peer in peers}  # Set up empty dict for peer IDs and ports

    # Wait for ports to be assigned
    while None in peer_ports.values():
        for peer in peers:
            if peer.port is not None:
                peer_ports[peer.peer_id] = peer.port  # Update the dictionary with the assigned port
        time.sleep(1)  # Sleep for 1 second to give time for ports to be assigned

    # Assign exactly 3 neighbors for each peer
    for peer in peers:
        available_neighbors = [p for p in peers if p.peer_id != peer.peer_id]
        peer_neighbors = random.sample(available_neighbors, 3)
        peer.neighbors = [p.port for p in peer_neighbors]  # Assign 3 neighbors

        # Add port mapping for each peer (for dynamic lookup)
        peer.port_mapping = peer_ports

        print(f"Peer {peer.peer_id} has neighbors {[p.port for p in peer_neighbors]}")

    return peers

def continue_search(buyer_peer, product_name, max_hops=3):
    """ This function lets the buyer continue searching for other sellers when one is out of stock """
    lookup_message = Message.lookup(buyer_id=buyer_peer.peer_id, product_name=product_name, hop_count=max_hops)
    
    # Send lookup to another neighbor
    if buyer_peer.neighbors:
        random_neighbor_port = random.choice(buyer_peer.neighbors)
        print(f"Buyer {buyer_peer.peer_id} is continuing search with a new lookup to neighbor on port {random_neighbor_port}")
        buyer_peer.send_message(random_neighbor_port, json.dumps(lookup_message))

def switch_product(seller_peer, products):
    """ This function allows sellers to switch products after running out of stock """
    seller_peer.product_name = random.choice(products)
    seller_peer.stock = 10  # Reset stock
    print(f"Seller {seller_peer.peer_id} is now selling {seller_peer.product_name} with 10 new items!")

if __name__ == "__main__":
    N = 6  # Number of peers can be passed as command line argument
    peers = initialize_peers(N)

    # Start all peers
    for peer in peers:
        peer.start()

    # Verify that all peers have valid ports
    for peer in peers:
        assert peer.port is not None, f"Peer {peer.peer_id} does not have a valid port assigned!"
        print(f"Peer {peer.peer_id} is using port {peer.port}")

    # Peer 0 (Buyer) sends a lookup message (random product search)
    buyer_products = ["fish", "salt", "boar"]
    selected_product = random.choice(buyer_products)  # Randomly selected product

    print(f"Buyer Peer 0 is looking for {selected_product}")
    lookup_message = Message.lookup(buyer_id=0, product_name=selected_product, hop_count=3)

    # Peer 0 sends a lookup message to one of its neighbors
    neighbor_port = peers[0].neighbors[0]  # Use one of the neighbors of peer 0
    peers[0].send_message(neighbor_port, json.dumps(lookup_message))

    # Example to handle search continuation and product switching
    # Buyer Peer 0 continues searching if out of stock, and sellers switch products when out of stock
    for peer in peers:
        if peer.role == "seller" and peer.stock == 0:
            switch_product(peer, buyer_products)  # Seller switches product if out of stock
        elif peer.role == "buyer":
            continue_search(peer, selected_product)  # Buyer keeps searching