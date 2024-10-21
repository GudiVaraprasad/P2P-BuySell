import json
import os
import threading
import time

# Path to Peer Registry json
peer_registry_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'network', 'peer_registry.json')

# Lock to synchronize file access
registry_lock = threading.Lock()


def initialize_registry():
    """Initialize the peer registry file to track connected peers."""
    with registry_lock:
        if not os.path.exists(peer_registry_file):
            with open(peer_registry_file, 'w') as f:
                json.dump({"connected_peers": 0, "peers": {}}, f)


def register_peer(peer_id, peer_ip):
    """Register a peer by adding it to the peer registry."""
    with registry_lock:
        with open(peer_registry_file, 'r+') as f:
            registry_data = json.load(f)
            registry_data['peers'][str(peer_id)] = {"ip": peer_ip, "port": None, "role": None, "neighbors": []}
            registry_data['connected_peers'] += 1
            
            # Update the registry file
            f.seek(0)
            json.dump(registry_data, f, indent=4)
            f.truncate()

    print(f"Peer {peer_id} with IP {peer_ip} registered successfully.")


def update_peer_info(peer_id, port=None, role=None, neighbors=None):
    """Update peer information in the registry (e.g., port, role, neighbors)."""
    with registry_lock:
        with open(peer_registry_file, 'r+') as f:
            registry_data = json.load(f)
            peer_info = registry_data['peers'].get(str(peer_id), {})

            if port is not None:
                peer_info['port'] = port
            if role is not None:
                peer_info['role'] = role
            if neighbors is not None:
                peer_info['neighbors'] = neighbors

            registry_data['peers'][str(peer_id)] = peer_info
            
            # Update the registry file
            f.seek(0)
            json.dump(registry_data, f, indent=4)
            f.truncate()

    print(f"Peer {peer_id} updated with port {port}, role {role}, and neighbors {neighbors}.")


def wait_for_all_peers(total_peers):
    """Wait for all peers to connect before proceeding."""
    print(f"Waiting for all {total_peers} peers to connect...")

    while True:
        with registry_lock:
            with open(peer_registry_file, 'r') as f:
                registry_data = json.load(f)
                connected_peers = registry_data.get('connected_peers', 0)

        if connected_peers >= total_peers:
            print(f"All {total_peers} peers have connected!")
            break

        time.sleep(2)  # Wait and check again