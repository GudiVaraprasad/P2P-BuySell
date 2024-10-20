from protocol.message import Message
import threading

def handle_lookup(peer, message):
    """Handle incoming lookup requests."""
    print(f"DEBUG: Entered handle_lookup for Peer {peer.peer_id} with message: {message}")

    # Prevent handling duplicate lookup requests by tracking request IDs (or timestamps)
    request_id = (message['buyer_id'], message['product_name'])
    if request_id in peer.processed_requests:
        print(f"DEBUG: Peer {peer.peer_id} has already processed request {request_id}. Ignoring duplicate.")
        return  # Ignore duplicate request
    else:
        peer.processed_requests.add(request_id)  # Track this request as processed

    if peer.role == "seller":
        # Check if the seller has the requested product
        with peer.lock:
            if message['product_name'] == peer.product_name and peer.stock > 0:
                print(f"DEBUG: Peer {peer.peer_id} is a seller. Proceeding to product check.")
                reply_message = Message.reply(
                    seller_id=peer.peer_id,
                    buyer_id=message['buyer_id'],
                    product_name=message['product_name'],
                    path=message.get('path', []) + [peer.peer_id]
                )
                buyer_port = peer.port_mapping.get(message['buyer_id'])
                if buyer_port:
                    peer.messaging_service.send_message(reply_message, buyer_port)
                    peer.stock -= 1
                    print(f"DEBUG: Peer {peer.peer_id} sold {message['product_name']}. Stock is now {peer.stock}.")
                else:
                    print(f"ERROR: Peer {peer.peer_id} could not find port for Buyer {message['buyer_id']}")
            else:
                print(f"DEBUG: Peer {peer.peer_id} does not have the requested product or is out of stock.")
    else:
        if message['hop_count'] > 0:
            message['hop_count'] -= 1
            message['path'].append(peer.peer_id)
            for neighbor_port in peer.neighbors:
                if neighbor_port != peer.port:
                    peer.messaging_service.send_message(message, neighbor_port)
        else:
            print(f"DEBUG: Peer {peer.peer_id} cannot forward message, hop_count reached 0.")
