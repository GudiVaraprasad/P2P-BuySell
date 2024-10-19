# main.py
from network.peer import Peer
from protocol.message import Message
import json 
import threading
import time

def initialize_peers():
    peers = [
        Peer(peer_id=0, role="buyer", neighbors=[], product_name=None),
        Peer(peer_id=1, role="seller", neighbors=[], product_name="fish", stock=10),
        Peer(peer_id=2, role="seller", neighbors=[], product_name="apple", stock=5),
        Peer(peer_id=3, role="buyer", neighbors=[], product_name=None),
        Peer(peer_id=4, role="seller", neighbors=[], product_name="fish", stock=8),
        Peer(peer_id=5, role="buyer", neighbors=[], product_name=None)
    ]

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

    # Now assign neighbors and port mapping to each peer
    for peer in peers:
        peer.neighbors = list(peer_ports.values())  # Assign all peer ports as neighbors
        peer.port_mapping = peer_ports  # Add port mapping for each peer (for dynamic lookup)

    return peers

if __name__ == "__main__":
    peers = initialize_peers()

    # Start all peers
    for peer in peers:
        peer.start()

    # Verify that all peers have valid ports
    for peer in peers:
        assert peer.port is not None, f"Peer {peer.peer_id} does not have a valid port assigned!"
        print(f"Peer {peer.peer_id} is using port {peer.port}")

    # Peer 0 (Buyer) sends a lookup message (random product search)
    buyer_products = ["fish", "salt"]
    selected_product = "fish"  # Randomly selected product for this example

    lookup_message = Message.lookup(buyer_id=0, product_name=selected_product, hop_count=3)

    # Peer 0 sends a lookup message to Peer 1
    peer_1_port = peers[1].port  # Use dynamically assigned port
    peers[0].send_message(peer_1_port, json.dumps(lookup_message))