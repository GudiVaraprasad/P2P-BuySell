# main.py
from network.network_manager import NetworkManager

def initialize_peers():
    peer_configs = [
        {"peer_id": 0, "role": "buyer", "port": 5000, "neighbors": [(1, 5001), (2, 5002)]},
        {"peer_id": 1, "role": "seller", "port": 5001, "neighbors": [(0, 5000), (3, 5003)]},
        {"peer_id": 2, "role": "seller", "port": 5002, "neighbors": [(0, 5000), (4, 5004)]},
        {"peer_id": 3, "role": "buyer", "port": 5003, "neighbors": [(1, 5001), (5, 5005)]},
        {"peer_id": 4, "role": "seller", "port": 5004, "neighbors": [(2, 5002), (5, 5005)]},
        {"peer_id": 5, "role": "buyer", "port": 5005, "neighbors": [(3, 5003), (4, 5004)]},
    ]
    return peer_configs

if __name__ == "__main__":
    peer_configs = initialize_peers()
    network_manager = NetworkManager(peer_configs)
    network_manager.start_network()
