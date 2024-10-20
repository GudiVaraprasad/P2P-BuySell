import random
import time
import threading
from network.peer import Peer

def initialize_peers(N):
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
    for peer_id, role in enumerate(peer_roles):
        if 'seller' in role:
            product_name = role.split('_')[0]
            stock = random.randint(2, 5)
            peers.append(Peer(peer_id=peer_id, role="seller", neighbors=[], product_name=product_name, stock=stock))
        else:
            peers.append(Peer(peer_id=peer_id, role="buyer", neighbors=[], product_name=None))

    for peer in peers:
        threading.Thread(target=peer.listen_for_requests).start()

    peer_ports = {peer.peer_id: None for peer in peers}

    while None in peer_ports.values():
        for peer in peers:
            if peer.port is not None:
                peer_ports[peer.peer_id] = peer.port
        time.sleep(1)

    # Assign neighbors and port mapping to each peer
    for peer in peers:
        peer.neighbors = random.sample(list(peer_ports.values()), min(3, N-1))
        peer.port_mapping = peer_ports  # Ensure port mapping is assigned here

    return peers