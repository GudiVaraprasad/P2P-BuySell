import threading

def handle_buy(peer, message):
    """Handle incoming buy requests."""
    print(f"Peer {peer.peer_id} (seller) received buy request from buyer {message['buyer_id']} for product {message['product_name']}")
    with peer.lock:
        if peer.stock > 0:
            peer.stock -= 1
            print(f"Seller {peer.peer_id} sold {message['product_name']} to Buyer {message['buyer_id']}")
            print(f"Seller {peer.peer_id} now has {peer.stock} items remaining")
        else:
            print(f"Seller {peer.peer_id} is out of stock!")
