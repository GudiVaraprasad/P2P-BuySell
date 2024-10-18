# network/network_manager.py
from network.peer import Peer

class NetworkManager:
    def __init__(self, peer_configs):
        self.peers = []

        # Create peers based on the configurations
        for config in peer_configs:
            peer = Peer(config['peer_id'], config['role'], config['port'], config['neighbors'])
            self.peers.append(peer)

    def start_network(self):
        for peer in self.peers:
            peer.start()

    def stop_network(self):
        for peer in self.peers:
            peer.stop()
