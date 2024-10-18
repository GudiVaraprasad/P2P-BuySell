# main.py
from network.peer import Peer

def initialize_peers():
    # Define peers with their roles, ports, and neighbors
    peer_configs = [
        {"peer_id": 0, "role": "buyer", "port": 5000, "neighbors": [(5001,), (5002,)]},
        {"peer_id": 1, "role": "seller", "port": 5001, "neighbors": [(5000,), (5003,)]},
        {"peer_id": 2, "role": "seller", "port": 5002, "neighbors": [(5000,), (5004,)]},
        {"peer_id": 3, "role": "buyer", "port": 5003, "neighbors": [(5001,), (5005,)]},
        {"peer_id": 4, "role": "seller", "port": 5004, "neighbors": [(5002,), (5005,)]},
        {"peer_id": 5, "role": "buyer", "port": 5005, "neighbors": [(5003,), (5004,)]}
    ]

    peers = []
    for config in peer_configs:
        peer = Peer(config['peer_id'], config['role'], config['port'], config['neighbors'])
        peers.append(peer)
    
    return peers

if __name__ == "__main__":
    peers = initialize_peers()
    
    # Start all peers
    for peer in peers:
        peer.start()
    
    # Keep the system running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Shutting down peers...")
        for peer in peers:
            peer.stop()
