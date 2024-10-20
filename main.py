import random
import time
import threading
from network.peer import Peer
from protocol.message import Message
import json

def initialize_peers(N):
    roles = ['fish_seller', 'salt_seller', 'boar_seller', 'buyer']

    # Randomly assign roles to peers while ensuring at least one buyer and one seller
    peer_roles = []
    has_buyer = False
    has_seller = False

    # Ensure at least one buyer and one seller
    for i in range(N):
        if not has_buyer:
            peer_roles.append('buyer')
            has_buyer = True
        elif not has_seller:
            seller_type = random.choice(roles[:-1])  # Randomly choose one of the seller types
            peer_roles.append(seller_type)
            has_seller = True
        else:
            # Randomly choose any role after ensuring at least one buyer and seller
            peer_roles.append(random.choice(roles))

    random.shuffle(peer_roles)  # Shuffle the roles to randomize assignment

    peers = []
    for peer_id, role in enumerate(peer_roles):
        if 'seller' in role:
            product_name = role.split('_')[0]  # Extract the product name (e.g., 'fish', 'salt', 'boar')
            stock = random.randint(2, 5)  # Random stock between 2 and 5
            peers.append(Peer(peer_id=peer_id, role="seller", neighbors=[], product_name=product_name, stock=stock))
        else:
            peers.append(Peer(peer_id=peer_id, role="buyer", neighbors=[], product_name=None))

    # Start listening for each peer in a separate thread
    for peer in peers:
        threading.Thread(target=peer.listen_for_requests).start()

    # Dynamically assign neighbors based on assigned ports
    peer_ports = {peer.peer_id: None for peer in peers}  # Set up dict for peer IDs and ports

    # Wait for ports to be assigned
    while None in peer_ports.values():
        for peer in peers:
            if peer.port is not None:
                peer_ports[peer.peer_id] = peer.port  # Update with the assigned port
        time.sleep(1)

    # Assign neighbors and port mapping to each peer
    for peer in peers:
        peer.neighbors = random.sample(list(peer_ports.values()), min(3, N-1))  # Assign 3 random neighbors
        peer.port_mapping = peer_ports  # Add port mapping for each peer

    return peers

def continue_search(buyer_peer, product_name, max_hops=3):
    print(f"Buyer Peer {buyer_peer.peer_id} is looking for {product_name}")
    lookup_message = Message.lookup(
        buyer_id=buyer_peer.peer_id, 
        product_name=product_name, 
        hop_count=max_hops
    )
    
    # Send to all neighbors
    for neighbor_port in buyer_peer.neighbors:
        buyer_peer.send_message(neighbor_port, json.dumps(lookup_message))

def switch_product(seller_peer, products):
    new_product = random.choice(products)
    seller_peer.product_name = new_product
    seller_peer.stock = random.randint(2, 5)   # Random stock between 2 and 5
    print(f"Seller {seller_peer.peer_id} now sells {new_product} with {seller_peer.stock} items remaining")

# New function to continuously search for products as a buyer
def buyer_behavior(buyer_peer, products):
    """Buyer continuously searches for products with random delays between searches."""
    while True:
        product_to_buy = random.choice(products)
        continue_search(buyer_peer, product_to_buy)
        
        # Wait for a random amount of time before the next search
        wait_time = random.randint(5, 7)  # Wait for 5 to 7 seconds
        print(f"Buyer {buyer_peer.peer_id} will wait {wait_time} seconds before the next purchase.")
        time.sleep(wait_time)

if __name__ == "__main__":
    N = 6  # Number of peers (you can make this a command-line argument)
    peers = initialize_peers(N)

    # Start all peers
    for peer in peers:
        peer.start()

    # Verify that all peers have valid ports
    for peer in peers:
        assert peer.port is not None, f"Peer {peer.peer_id} does not have a valid port assigned!"
        print(f"Peer {peer.peer_id} is using port {peer.port} with role {peer.role}")

    # Peer 0 (Buyer) sends a lookup message (random product search)
    buyer_peers = [peer for peer in peers if peer.role == 'buyer']
    seller_peers = [peer for peer in peers if peer.role == 'seller']
    
    # Let the buyers start searching for products continuously
    products = ['fish', 'salt', 'boar']
    
    for buyer in buyer_peers:
        threading.Thread(target=buyer_behavior, args=(buyer, products)).start()  # Start buyer behavior in threads

    # Simulate some sellers selling out and switching products
    time.sleep(5)  # Wait for some transactions
    for seller in seller_peers:
        if seller.stock <= 0:
            switch_product(seller, products)