import json
import threading
import time  # Import time for sleep
from network.peer import Peer
from protocol.message import Message

def initialize_peers():
    # Initialize peers without pre-defining ports
    peers = [
        Peer(peer_id=0, role="buyer", neighbors=[], product_name=None),
        Peer(peer_id=1, role="seller", neighbors=[], product_name="fish", stock=10)
    ]
    
    # Start listening for each peer in a separate thread and store the assigned port
    for peer in peers:
        threading.Thread(target=peer.listen_for_requests).start()

    # Allow time for peers to bind their ports dynamically
    time.sleep(1)  # Wait for 1 second to allow port assignment

    # Dynamically assign neighbors based on assigned ports
    peer_0_port = peers[0].port
    peer_1_port = peers[1].port

    # After ensuring the ports are assigned, set the neighbors
    peers[0].neighbors.append(peer_1_port)  # Peer 0 has Peer 1 as a neighbor
    peers[1].neighbors.append(peer_0_port)  # Peer 1 has Peer 0 as a neighbor

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

    # Peer 0 sends a lookup message to Peer 1 (looking for fish)
    lookup_message = Message.lookup(buyer_id=0, product_name="fish", hop_count=3)

    # Peer 0 sends a lookup message to Peer 1
    peer_1_port = peers[1].port  # Use dynamically assigned port
    peers[0].send_message(peer_1_port, json.dumps(lookup_message))