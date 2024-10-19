# main.py
from network.peer import Peer
from protocol.message import Message
import json 
import threading

def initialize_peers():
    peers = [
        Peer(peer_id=0, role="buyer", port=5000, neighbors=[5001]),
        Peer(peer_id=1, role="seller", port=5001, neighbors=[5000])
    ]
    
    # Start listening for each peer in a separate thread
    for peer in peers:
        threading.Thread(target=peer.listen_for_requests).start()

    return peers

if __name__ == "__main__":
    peers = initialize_peers()

    # Start all peers
    for peer in peers:
        peer.start()

    # Peer 0 sends a lookup message to Peer 1 (looking for fish)
    lookup_message = Message.lookup(buyer_id=0, product_name="fish", hop_count=3)
    peers[0].send_message(5001, json.dumps(lookup_message))

